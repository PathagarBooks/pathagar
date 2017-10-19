import os

from django.conf.urls import include, url
#from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

from django.conf import settings
from pathagar.books.app_settings import BOOKS_STATICS_VIA_DJANGO


urlpatterns = [

    # Book list:
    url(r'^$', 'pathagar.books.views.home',
     kwargs={}, name='home'),
    url(r'^latest/$', 'pathagar.books.views.latest',
     {}, 'latest'),
    url(r'^by-title/$', 'pathagar.books.views.by_title',
     {}, 'by_title'),
    url(r'^by-author/$', 'pathagar.books.views.by_author',
     {}, 'by_author'),
    url(r'^by-author/(?P<author_id>\d+)/$', 'pathagar.books.views.by_title',
     {}, 'books_by_author'),
    url(r'^tags/(?P<tag>.+)/$', 'pathagar.books.views.by_tag',
     {}, 'by_tag'),
    url(r'^by-popularity/$', 'pathagar.books.views.most_downloaded',
     {}, 'most_downloaded'),

    # Tag groups:
    url(r'^tags/groups.atom$', 'pathagar.books.views.tags_listgroups',
     {}, 'tags_listgroups'),

    # Book list Atom:
    url(r'^catalog.atom$', 'pathagar.books.views.root',
     {'qtype': u'feed'}, 'root_feed'),
    url(r'^latest.atom$', 'pathagar.books.views.latest',
     {'qtype': u'feed'}, 'latest_feed'),
    url(r'^by-title.atom$', 'pathagar.books.views.by_title',
     {'qtype': u'feed'}, 'by_title_feed'),
    url(r'^by-author.atom$', 'pathagar.books.views.by_author',
     {'qtype': u'feed'}, 'by_author_feed'),
    url(r'^by-author/(?P<author_id>\d+).atom$', 'pathagar.books.views.by_title',
     {'qtype': u'feed'}, 'by_author_feed'),
    url(r'^tags/(?P<tag>.+).atom$', 'pathagar.books.views.by_tag',
     {'qtype': u'feed'}, 'by_tag_feed'),
    url(r'^by-popularity.atom$', 'pathagar.books.views.most_downloaded',
     {'qtype': u'feed'}, 'most_downloaded_feed'),

    # Tag groups:
    url(r'^tags/groups/(?P<group_slug>[-\w]+)/$', 'pathagar.books.views.tags',
     {}, 'tag_groups'),

    url(r'^tags/groups/(?P<group_slug>[-\w]+).atom$', 'pathagar.books.views.tags',
     {'qtype': u'feed'}, 'tag_groups_feed'),

    # Tag list:
    url(r'^tags/$', 'pathagar.books.views.tags', {}, 'tags'),
    url(r'^tags.atom$', 'pathagar.books.views.tags',
     {'qtype': u'feed'}, 'tags_feed'),


    # Add, view, edit and remove books:
    url(r'^book/add$', 'pathagar.books.views.add_book'),
    url(r'^book/(?P<book_id>\d+)/view$', 'pathagar.books.views.book_detail'),
    url(r'^book/(?P<book_id>\d+)/edit$', 'pathagar.books.views.edit_book'),
    url(r'^book/(?P<book_id>\d+)/remove$', 'pathagar.books.views.remove_book'),
    url(r'^book/(?P<book_id>\d+)/download$', 'pathagar.books.views.download_book'),

    # Comments
    # FIXME (r'^comments/', include('django.contrib.comments.urls')),

    # Add language:
    url(r'^add/dc_language|language/$', 'pathagar.books.views.add_language'),

    # Auth login and logout:
    url(r'^accounts/login/$', 'django.contrib.auth.views.login'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout'),

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
