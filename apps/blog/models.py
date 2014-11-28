# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from datetime import datetime
from apps.profiles.models import Profile
from django.db.models import Q
from apps.blog.tasks import resize_image
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic


class BaseComment(models.Model):
    content = models.TextField(_("Content"), null=True, blank=True)
    date = models.DateTimeField(_("Date Started"), default=datetime.now())
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey("content_type", "object_id")

    class Meta:
        abstract = True
        ordering = ("-date",)


class PostComment(BaseComment):
    writer = models.ForeignKey(Profile, verbose_name=_("Profile"),
                               null=True, blank=True)
    anonymous_name = models.CharField(_(
        "Name"), max_length=50, null=True, blank=True)
    anonymous_mail = models.EmailField(_("E-mail"), null=True, blank=True)
    is_verified = models.BooleanField(_("Is Verified ?"), default=False)
    activation_key = models.CharField(_(
        "Activation Key"), max_length=40, null=True, blank=True)

    def __unicode__(self):
        return u"%s" % self.name

    def name(self):
        if self.writer:
            return self.writer
        else:
            return self.anonymous_name

    name = property(name)

    def get_children(self):
        comments = PostComment.objects.select_related().filter(
            Q(writer__isnull=False) | Q(is_verified=True),
            content_type=ContentType.objects.get_for_model(self),
            object_id=self.id)
        return comments


class Post(models.Model):
    author = models.ForeignKey(Profile, verbose_name=_("Author"))
    title = models.CharField(_("Title"), max_length=75)
    content = models.TextField(_("Content"))
    date = models.DateTimeField(_("Date"), default=datetime.now())
    picture = models.ImageField(_(
        "Post Picture"), upload_to="postimages/", null=True, blank=True)
    comments = generic.GenericRelation(PostComment)

    def __unicode__(self):
        return u"%s" % self.title

    def comment_count(self):
        return self.comments.filter(
            Q(writer__isnull=False) | Q(is_verified=True)).count()

    def save(self, *args, **kwargs):
        super(Post, self).save(*args, **kwargs)
        if self.picture:
            resize_image.delay(self.picture.path)

    class Meta:
        verbose_name = _("Post")
        verbose_name_plural = _("Posts")
        ordering = ("-date",)






