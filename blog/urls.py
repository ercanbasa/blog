from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import password_change, password_change_done
from apps.blog.views import *
from apps.profiles.views import *

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', Home.as_view(), name='home'),
    # profile urls
    url(r'^logout/$', logout_user, name='logout'),
    url(r'^register/$', register, name='register'),
    url(r'^login/$', login_user, name='login'),
    url(r'^profile/$', profile, name='profile'),
    url(r'^profile/update/$', login_required(
        ProfileUpdate.as_view()), name='profile_update'),
    url(r'^profile/password/update/$', login_required(password_change),
        {'template_name': 'password_update.html',
         'post_change_redirect': 'profile/update_completed/'},
        name='password_update'),
    url(r'^profile/update_completed/$', login_required(password_change_done),
        {'template_name': 'update_successfull.html'}, name='update_completed'),
    url(r'^profile/email/update/$', email_update, name='email_update'),
    url(r'^profile/activation/(?P<key>\w+)/$',
        activate_user, name='activation'),
    url(r'^profile/delete/$', delete_user, name='delete_user'),

    # post urls
    url(r'^post/(?P<pk>\d+)/$', post_detail, name='post_detail'),
    url(r'^post/create/$', login_required(
        PostCreate.as_view()), name='create_post'),
    url(r'^post/(?P<post_id>\d+)/comment/(?P<key>\w+)/activation/$',
        activate_comment, name='comment_activation'),
    url(r'^post/(?P<pk>\d+)/comment/create/$', comment_to_comment,
        name='comment_to_comment'),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^uploads/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    )
