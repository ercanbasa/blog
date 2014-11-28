# -*- coding: utf-8 -*-
from django import template
from django.template import Context, loader
from django.db.models import Q

register = template.Library()


@register.assignment_tag(takes_context=True)
def comment_tree(context, post=None):
    qs = post.comments.filter(Q(writer__isnull=False) | Q(
        is_verified=True)).select_related()
    t = loader.get_template("inc/comments.html")
    c = Context({'post_comments': qs})
    return t.render(c)
