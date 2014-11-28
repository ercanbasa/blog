# -*- coding: utf-8 -*-
from apps.profiles.models import Profile
from django.contrib.auth.models import User
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext
from django.contrib.auth.forms import AuthenticationForm


class RegistrationForm(forms.Form):
    email = forms.EmailField(label=_("E-Mail"), max_length=75)
    first_name = forms.CharField(label=_("Name"), max_length=30)
    last_name = forms.CharField(label=_("Last Name"), max_length=30)
    about = forms.CharField(label=_("About Me"), widget=forms.Textarea)
    password1 = forms.CharField(label=_(
        "Password"), widget=forms.PasswordInput())
    password2 = forms.CharField(label=_(
        "Password (Again)"), widget=forms.PasswordInput())

    def clean_password2(self):
        if 'password1' in self.cleaned_data:
            password1 = self.cleaned_data['password1']
            password2 = self.cleaned_data['password2']
            if password1 == password2:
                return password2
        raise forms.ValidationError(ugettext('Passwords do not match.'))

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            User.objects.get(email=email)
            raise forms.ValidationError(ugettext('E-Mail is already used.'))
        except User.DoesNotExist:
            return email
            

class ProfileForm(forms.ModelForm):

    first_name = forms.CharField(label=_("Name"), max_length=30)
    last_name = forms.CharField(label=_("Last Name"), max_length=30)

    class Meta:
        model = Profile
        exclude = ('user', 'is_deleted', 'is_verified', 'activation_key')


class LoginForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields["username"].label = "E-Mail"
        self.fields["username"].max_length = 75
        self.fields["username"].widget.attrs = {"maxlength": 75}
        self.fields["username"].validators[0].limit_value = 75
        self.error_messages = {
            'invalid_login': _("Please enter a correct e-mail and password. "
                               "Note that both fields may be case-sensitive."),
            'inactive': _("This account is inactive."),
        }


class EmailUpdateForm(forms.Form):
    email1 = forms.EmailField(label=_("E-Mail"), max_length=30)
    email2 = forms.EmailField(label=_("E-Mail (Again)"), max_length=30)

    def clean_email2(self):
        if 'email1' in self.cleaned_data:
            email1 = self.cleaned_data['email1']
            email2 = self.cleaned_data['email2']
            if email1 == email2:
                return email2
        raise forms.ValidationError(ugettext('E-Mails do not match.'))
