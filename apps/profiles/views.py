# -*- coding: utf-8 -*-
import random
import hashlib
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.contrib.auth import logout, login, authenticate
from django.http import HttpResponse
from django.views.generic.edit import UpdateView
from apps.profiles.models import Profile
from apps.profiles.forms import (RegistrationForm, ProfileForm,
                                 LoginForm, EmailUpdateForm)
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils.translation import ugettext as _
from apps.blog.tasks import mail_sender
from django.core.cache import cache
from apps.profiles.decorators import anonymous_required


@login_required
def logout_user(request):
    logout(request)
    return redirect('home')


@anonymous_required('home')
def register(request, template="register.html"):
    if not request.method == "POST":
        form = RegistrationForm()
    else:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=hashlib.sha1(str(random.random())).hexdigest()[:30],
                password=form.cleaned_data['password1'],
                email=form.cleaned_data['email']
            )
            user.first_name = form.cleaned_data["first_name"]
            user.last_name = form.cleaned_data["last_name"]
            user.is_active = False
            user.save()

            about = form.cleaned_data["about"]
            profile = Profile.objects.create(user=user, about=about)
            profile.activation_key = hashlib.sha1(
                str(random.random())).hexdigest()
            profile.save()

            subject = 'New User Email Confirmation'
            message = """Hello %s,\nConfirm your account via the link below\n
                %s%s""" % (
                user.get_full_name(),
                request.META['HTTP_ORIGIN'],
                reverse('activation', kwargs={'key': profile.activation_key}))
            sender = 'noreply.djangoblog@gmail.com'
            recipients = [user.email]
            mail_sender.delay(subject, message, sender, recipients)

            messages.add_message(
                request, messages.SUCCESS,
                _("Your profile has been created! Confirm your account with"
                  " activation key from your mail."))

            return redirect('register')

    return render(request, template, {'form': form})


@anonymous_required('home')
def login_user(request, template="login.html"):
    if not request.method == "POST":
        form = LoginForm()
    else:
        form = LoginForm(None, request.POST)
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(email=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('home')

    return render(request, template, {'form': form})


@login_required
def profile(request, template="profile.html"):
    profile = Profile.objects.from_request(request)
    posts = cache.get('profile_%s' % profile.id)
    if posts is None:
        posts = profile.post_set.all()
        cache.set('profile_%s' % profile.id, posts, nx=True)

    ctx = {
        'profile': profile,
        'posts': posts,
    }
    return render(request, template, ctx)


class ProfileUpdate(UpdateView):
    template_name = "profile_update.html"
    model = Profile
    form_class = ProfileForm

    def get_object(self, queryset=None):
        obj = Profile.objects.from_request(self.request)
        return obj

    def get_initial(self):
        """ get the initial value for user.email """
        init = super(ProfileUpdate, self).get_initial()
        user = self.request.user
        init.update({
            'first_name': user.first_name,
            'last_name': user.last_name,
        })
        return init

    def get_success_url(self):
        return reverse('profile_update')

    def form_valid(self, form):
        self.object = form.instance
        first_name = form.cleaned_data.get('first_name')
        last_name = form.cleaned_data.get('last_name')
        self.object.user.first_name = first_name
        self.object.user.last_name = last_name
        self.object.user.save()
        messages.add_message(self.request, messages.SUCCESS,
                             _('Your profile has been updated successfully!')
                             )
        return super(ProfileUpdate, self).form_valid(form)


@login_required
def email_update(request, template="email_update.html"):
    if not request.method == "POST":
        form = EmailUpdateForm()
    else:
        form = EmailUpdateForm(request.POST)
        if form.is_valid():
            user = request.user
            email = form.cleaned_data['email1']
            user.email = email
            user.is_active = False
            user.save()
            profile = Profile.objects.from_request(request)
            profile.activation_key = hashlib.sha1(
                str(random.random())).hexdigest()
            profile.is_verified = False
            profile.save()

            subject = 'User New Email Confirmation'
            message = """
                Hello %s,\nConfirm your new email via the link below\n
                http://%s%s""" % (
                user.get_full_name(),
                request.META['HTTP_HOST'],
                reverse('activation', kwargs={'key': profile.activation_key}))
            sender = 'noreply.djangoblog@gmail.com'
            recipients = [user.email]
            mail_sender.delay(subject, message, sender, recipients)

            logout(request)
            messages.add_message(
                request, messages.SUCCESS,
                _('Your email has been updated! Please confirm your email.'))
            return redirect('home')

    return render(request, template, {'form': form})


def activate_user(request, key=None):
    profile = get_object_or_404(
        Profile.objects.select_related(), activation_key=key)
    if profile.is_verified:
        return HttpResponse(
            _("This profile is already activated"),
            content_type="text/plain")
    else:
        usr = profile.user
        profile.is_verified = True
        usr.is_active = True
        usr.save()
        profile.save()
        return HttpResponse(
            _("Your profile has been activated successfully!"),
            content_type="text/plain")


@login_required
def delete_user(request):
    profile = Profile.objects.from_request(request)
    profile.is_deleted = True
    request.user.is_active = False
    request.user.save()
    profile.save()
    logout(request)
    messages.add_message(request, messages.SUCCESS,
                         _('Your account has been deleted!'))
    return redirect('home')
