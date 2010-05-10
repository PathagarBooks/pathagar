import os

from django.conf.urls.defaults import *
from django.views.static import serve
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

import settings

urlpatterns = patterns('',
    # Example:
    # (r'^pathagar/', include('pathagar.foo.urls')),

    (r'^catalogs/', 'pathagar.books.views.catalogs'),
    (r'^books/(?P<path>.*)$', serve, {'document_root': os.path.join(settings.MEDIA_ROOT, 'books')}),
    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^addbook/','pathagar.books.views.add_book'),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
)
