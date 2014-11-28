# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from datetime import datetime


class ProfileManager(models.Manager):

    def from_request(self, request, *args, **kwargs):
        try:
            return self.select_related().get(user=request.user)
        except User.DoesNotExist:
            return None


class Profile(models.Model):
    user = models.OneToOneField(User, verbose_name=_("User"))
    about = models.TextField(_("About Me"))
    is_deleted = models.BooleanField(_("Is Deleted ?"), default=False)
    is_verified = models.BooleanField(_("Is Verified ?"), default=False)
    activation_key = models.CharField(_(
        "Activation Key"), max_length=40, null=True, blank=True)

    objects = ProfileManager()

    def __unicode__(self):
        return u"%s" % (self.user.get_full_name())
