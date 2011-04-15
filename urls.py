import os

from django.conf.urls.defaults import *
from django.contrib import admin
admin.autodiscover()

from django.conf import settings
from pathagar.books.app_settings import BOOKS_STATICS_VIA_DJANGO

urlpatterns = patterns('',
    
    # Book list:
    (r'^$', 'pathagar.books.views.latest', {}, 'latest'),
    (r'^by-title/$', 'pathagar.books.views.by_title', {}, 'by_title'),
    (r'^by-author/$', 'pathagar.books.views.by_author', {}, 'by_author'),
    (r'^tags/(?P<tag>[-\w]+)/$', 'pathagar.books.views.by_tag', {}, 'by_tag'),
    
    # Book list Atom:
    (r'^feed.atom', 'pathagar.books.views.latest',
     {'qtype': u'feed'}, 'latest_feed'),
    (r'^by-title.atom$', 'pathagar.books.views.by_title',
     {'qtype': u'feed'}, 'by_title_feed'),
    (r'^by-author.atom$', 'pathagar.books.views.by_author',
     {'qtype': u'feed'}, 'by_author_feed'),
    (r'^tags/(?P<tag>[-\w]+).atom$', 'pathagar.books.views.by_tag',
     {'qtype': u'feed'}, 'by_tag_feed'),
        
    # Tag list:
    (r'^tags/', 'pathagar.books.views.tags', {}, 'tags'),
    
    # Add, view, edit and remove books:
    (r'^add/book/?$', 'pathagar.books.views.add_book'),
    (r'^view/book/(?P<book_id>\d+)/$', 'pathagar.books.views.book_detail'),
    (r'^edit/book/(?P<book_id>\d+)/?$', 'pathagar.books.views.edit_book'),
    (r'^remove/book/(?P<book_id>\d+)/?$', 'pathagar.books.views.remove_book'),
    
    # Add language:
    (r'^add/dc_language|language/?$', 'pathagar.books.views.add_language'),
    
    # Auth login and logout:
    (r'^accounts/login/$', 'django.contrib.auth.views.login'),
    (r'^accounts/logout/$', 'django.contrib.auth.views.logout'),
    
    # Admin:
    (r'^admin/', include(admin.site.urls)),
)


if BOOKS_STATICS_VIA_DJANGO:
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
