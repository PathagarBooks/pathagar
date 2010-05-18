import os

from django.conf.urls.defaults import *
from django.views.static import serve
from settings import MEDIA_ROOT
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

import settings

urlpatterns = patterns('',
    # Example:
    # (r'^pathagar/', include('pathagar.foo.urls')),

    (r'^$', 'pathagar.books.views.page'),
    (r'^view/book/(?P<book_id>\d+)/$', 'pathagar.books.views.book_details'),

    (r'^catalogs/', 'pathagar.books.views.catalogs'),
    (r'^books/(?P<path>.*)$', serve, {'document_root': os.path.join(settings.MEDIA_ROOT, 'books')}),
    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^add/book/?$', 'pathagar.books.views.add_book'),
    (r'^add/dc_language|language/?$', 'pathagar.books.views.add_language'),
    (r'^accounts/login/$', 'django.contrib.auth.views.login'),
    (r'^static_media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': MEDIA_ROOT, 'show_indexes': True}),


    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
)
