# -*- coding: utf-8 -*-
from django.contrib import admin
from apps.blog.models import *

admin.site.register(Post)
admin.site.register(PostComment)
