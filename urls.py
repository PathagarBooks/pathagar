import os

from django.conf.urls.defaults import *
from django.contrib import admin
admin.autodiscover()

import settings

urlpatterns = patterns('',
    
    # Index page:
    (r'^$', 'pathagar.books.views.book_list'),
    (r'^by-title/$', 'pathagar.books.views.by_title'),
    (r'^by-author/$', 'pathagar.books.views.by_author'),
    
    # Add, view, edit and remove books:
    (r'^add/book/?$', 'pathagar.books.views.add_book'),
    (r'^view/book/(?P<book_id>\d+)/$', 'pathagar.books.views.book_detail'),
    (r'^edit/book/(?P<book_id>\d+)/?$', 'pathagar.books.views.edit_book'),
    (r'^remove/book/(?P<book_id>\d+)/?$', 'pathagar.books.views.remove_book'),
    
    # Atom books catalogs:
    (r'^catalogs/', 'pathagar.books.views.catalogs'),
    
    # Add language:
    (r'^add/dc_language|language/?$', 'pathagar.books.views.add_language'),
    
    # Auth:
    (r'^accounts/login/$', 'django.contrib.auth.views.login'),
    (r'^accounts/logout/$', 'django.contrib.auth.views.logout'),
    
    # Admin:
    (r'^admin/', include(admin.site.urls)),
)


if settings.DEBUG:
    from django.views.static import serve
    # Serve static media:
    urlpatterns += patterns('',
       url(r'^static_media/(?P<path>.*)$', serve,
           {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),

       # Book files and covers:
       url(r'^books/(?P<path>.*)$', serve,
           {'document_root': os.path.join(settings.MEDIA_ROOT, 'books')}),
       url(r'^covers/(?P<path>.*)$', serve,
           {'document_root': os.path.join(settings.MEDIA_ROOT, 'covers')}),
    )
