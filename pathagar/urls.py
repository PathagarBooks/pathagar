import os

from django.conf.urls import include, url
#from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

from django.conf import settings
from books.app_settings import BOOKS_STATICS_VIA_DJANGO

from django.contrib.auth import views as auth_views

urlpatterns = [

    url(r'', include('books.urls')),


    # Comments
    # FIXME (r'^comments/', include('django.contrib.comments.urls')),

    # Auth login and logout:
    url(r'^accounts/login/$', auth_views.login, name='login'),
    url(r'^accounts/logout/$', auth_views.logout, name='logout'),

    # Admin:
    url(r'^admin/', include(admin.site.urls)),
]


if BOOKS_STATICS_VIA_DJANGO:
    from django.views.static import serve
    # Serve static media:
    # urlpatterns += patterns('',
    urlpatterns += [
       url(r'^static_media/(?P<path>.*)$', serve,
           {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),

       # Book covers:
       url(r'^covers/(?P<path>.*)$', serve,
           {'document_root': os.path.join(settings.MEDIA_ROOT, 'covers')}),
    ]
