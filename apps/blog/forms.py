# -*- coding: utf-8 -*-
from django import forms
from apps.blog.models import Post, PostComment


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        exclude = ('author', 'date',)


class AnonymousCommentForm(forms.ModelForm):

    class Meta:
        model = PostComment
        fields = ('anonymous_name', 'anonymous_mail', 'content')

    def __init__(self, *args, **kwargs):
        super(AnonymousCommentForm, self).__init__(*args, **kwargs)
        self.fields['anonymous_name'].required = True
        self.fields['anonymous_mail'].required = True



class CommentForm(forms.ModelForm):

    class Meta:
        model = PostComment
        fields = ('content',)

