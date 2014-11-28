# -*- coding: utf-8 -*-
import random
import hashlib
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from django.core.urlresolvers import reverse
from apps.blog.models import Post, PostComment
from apps.profiles.models import Profile
from apps.blog.forms import (PostForm, AnonymousCommentForm,
                             CommentForm)
from django.contrib import messages
from django.utils.translation import ugettext as _
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.core.cache import cache
from apps.blog.tasks import mail_sender


class Home(TemplateView):
    template_name = "home.html"

    def get_context_data(self):
        context = super(Home, self).get_context_data()
        context['posts'] = Post.objects.all()
        return context


def post_detail(request, template="post_detail.html", pk=None):
    post = get_object_or_404(Post, pk=pk)
    ctx = {'post': post}

    if not request.method == "POST":
        if request.user.is_authenticated():
            form = CommentForm()
        else:
            form = AnonymousCommentForm()

    else:
        if request.user.is_authenticated():
            form = CommentForm(request.POST)
        else:
            form = AnonymousCommentForm(request.POST)

        if form.is_valid():
            obj = form.instance
            obj.content_object = post
            if request.user.is_authenticated():
                obj.writer = Profile.objects.from_request(request)
                messages.add_message(
                    request,
                    messages.SUCCESS,
                    _("Your comment has been saved successfully."))
            else:
                obj.activation_key = hashlib.sha1(
                    str(random.random())).hexdigest()
                obj.is_verified = False

                subject = 'Email confirmation'
                message = """
                    Hello %s,\nConfirm your comment via the link below\n
                    http://%s%s""" % (
                    obj.anonymous_name,
                    request.META['HTTP_HOST'],
                    reverse('comment_activation',
                            kwargs={'key': obj.activation_key,
                                    'post_id': post.id}))
                sender = 'noreply.djangoblog@gmail.com'
                recipients = [obj.anonymous_mail]
                mail_sender.delay(subject, message, sender, recipients)

                messages.add_message(
                    request,
                    messages.SUCCESS,
                    _("Your comment has been saved but it will not be "
                      "shown before your mail confirmation."))
            obj.save()

        if request.user.is_authenticated():
            form = CommentForm()
        else:
            form = AnonymousCommentForm()

    ctx.update({'form': form})
    return render(request, template, ctx)


class PostCreate(CreateView):
    template_name = "create_post.html"
    model = Post
    form_class = PostForm

    def get_success_url(self):
        return reverse('home')

    def form_valid(self, form):
        self.object = form.instance
        profile = Profile.objects.from_request(self.request)
        self.object.author = profile
        self.object.save()
        cache.delete('profile_%s' % profile.id)
        messages.add_message(self.request, messages.SUCCESS,
                             _('Your post has been saved successfully!'))
        return super(PostCreate, self).form_valid(form)


def activate_comment(request, key=None, post_id=None):
    comment = get_object_or_404(PostComment, activation_key=key)
    post = get_object_or_404(Post, pk=post_id)
    if comment.is_verified:
        return HttpResponse(_("This comment is already activated"),
                            content_type="text/plain")
    else:
        comment.is_verified = True
        comment.save()
        messages.add_message(request, messages.SUCCESS,
                             _('Your post has been activated successfully!'))
    return redirect('post_detail', pk=post.id)


def comment_to_comment(request,
                       template="comment_to_comment.html",
                       pk=None):
    comment = get_object_or_404(PostComment, pk=pk)
    post_id = comment.object_id

    if not request.method == "POST":
        if request.user.is_authenticated():
            form = CommentForm()
        else:
            form = AnonymousCommentForm()

    else:
        if request.user.is_authenticated():
            form = CommentForm(request.POST)
        else:
            form = AnonymousCommentForm(request.POST)

        if form.is_valid():
            obj = form.instance
            obj.content_object = comment
            if request.user.is_authenticated():
                obj.writer = Profile.objects.from_request(request)
                messages.add_message(
                    request,
                    messages.SUCCESS,
                    _("Your comment has been saved successfully."))
            else:
                obj.activation_key = hashlib.sha1(
                    str(random.random())).hexdigest()
                obj.is_verified = False

                subject = 'Email confirmation'
                message = """
                    Hello %s,\nConfirm your comment via the link below\n
                    http://%s%s""" % (
                    obj.anonymous_name,
                    request.META['HTTP_HOST'],
                    reverse('comment_activation',
                            kwargs={'key': obj.activation_key,
                                    'post_id': post_id}))
                sender = 'noreply.djangoblog@gmail.com'
                recipients = [obj.anonymous_mail]
                mail_sender.delay(subject, message, sender, recipients)

                messages.add_message(
                    request,
                    messages.SUCCESS,
                    _("Your comment has been saved but it will not be "
                      "shown before your mail confirmation."))
            obj.save()
            return redirect('post_detail', pk=post_id)

    ctx = {'form': form}
    return render(request, template, ctx)