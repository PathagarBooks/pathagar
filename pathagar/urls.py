import os

from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

from django.conf import settings
from books.app_settings import BOOKS_STATICS_VIA_DJANGO
from books.views import AddBookView, BookDetailView, EditBookView, RemoveBookView

urlpatterns = patterns('',

    # Book list:
    (r'^$', 'books.views.home',
     {}, 'home'),
    (r'^latest/$', 'books.views.latest',
     {}, 'latest'),
    (r'^by-title/$', 'books.views.by_title',
     {}, 'by_title'),
    (r'^by-author/$', 'books.views.by_author',
     {}, 'by_author'),
    (r'^tags/(?P<tag>.+)/$', 'books.views.by_tag',
     {}, 'by_tag'),
    (r'^by-popularity/$', 'books.views.most_downloaded',
     {}, 'most_downloaded'),

    # Tag groups:
    (r'^tags/groups.atom$', 'books.views.tags_listgroups',
     {}, 'tags_listgroups'),

    # Book list Atom:
    (r'^catalog.atom$', 'books.views.root',
     {'qtype': u'feed'}, 'root_feed'),
    (r'^latest.atom$', 'books.views.latest',
     {'qtype': u'feed'}, 'latest_feed'),
    (r'^by-title.atom$', 'books.views.by_title',
     {'qtype': u'feed'}, 'by_title_feed'),
    (r'^by-author.atom$', 'books.views.by_author',
     {'qtype': u'feed'}, 'by_author_feed'),
    (r'^tags/(?P<tag>.+).atom$', 'books.views.by_tag',
     {'qtype': u'feed'}, 'by_tag_feed'),
    (r'^by-popularity.atom$', 'books.views.most_downloaded',
     {'qtype': u'feed'}, 'most_downloaded_feed'),

    # Tag groups:
    (r'^tags/groups/(?P<group_slug>[-\w]+)/$', 'books.views.tags',
     {}, 'tag_groups'),

    (r'^tags/groups/(?P<group_slug>[-\w]+).atom$', 'books.views.tags',
     {'qtype': u'feed'}, 'tag_groups_feed'),

    # Tag list:
    (r'^tags/$', 'books.views.tags', {}, 'tags'),
    (r'^tags.atom$', 'books.views.tags',
     {'qtype': u'feed'}, 'tags_feed'),


    # Add, view, edit and remove books:
    url(r'^book/add$', AddBookView.as_view(), name='book-create'),
    url(r'^book/(?P<book_id>\d+)/view$', BookDetailView.as_view(), name='book-detail'),
    url(r'^book/(?P<book_id>\d+)/edit$', EditBookView.as_view(), name='book-edit'),
    url(r'^book/(?P<book_id>\d+)/remove$', RemoveBookView.as_view(), name='book-remove'),
    (r'^book/(?P<book_id>\d+)/download$', 'books.views.download_book'),

    # Comments
    (r'^comments/', include('django.contrib.comments.urls')),

    # Add language:
    (r'^add/dc_language|language/$', 'books.views.add_language'),

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

       # Book covers:
       url(r'^covers/(?P<path>.*)$', serve,
           {'document_root': os.path.join(settings.MEDIA_ROOT, 'covers')}),
    )
