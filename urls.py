import os

from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
admin.autodiscover()

from django.conf import settings
from pathagar.books.app_settings import BOOKS_STATICS_VIA_DJANGO

urlpatterns = patterns('',

    # Book list:
    (r'^$', 'pathagar.books.views.home',
     {}, 'home'),
    (r'^latest/$', 'pathagar.books.views.latest',
     {}, 'latest'),
    (r'^by-title/$', 'pathagar.books.views.by_title',
     {}, 'by_title'),
    (r'^by-author/$', 'pathagar.books.views.by_author',
     {}, 'by_author'),
    (r'^tags/(?P<tag>.+)/$', 'pathagar.books.views.by_tag',
     {}, 'by_tag'),
    (r'^by-popularity/$', 'pathagar.books.views.most_downloaded',
     {}, 'most_downloaded'),

    # Tag groups:
    (r'^tags/groups.atom$', 'pathagar.books.views.tags_listgroups',
     {}, 'tags_listgroups'),

    # Book list Atom:
    (r'^catalog.atom$', 'pathagar.books.views.root',
     {'qtype': u'feed'}, 'root_feed'),
    (r'^latest.atom$', 'pathagar.books.views.latest',
     {'qtype': u'feed'}, 'latest_feed'),
    (r'^by-title.atom$', 'pathagar.books.views.by_title',
     {'qtype': u'feed'}, 'by_title_feed'),
    (r'^by-author.atom$', 'pathagar.books.views.by_author',
     {'qtype': u'feed'}, 'by_author_feed'),
    (r'^tags/(?P<tag>.+).atom$', 'pathagar.books.views.by_tag',
     {'qtype': u'feed'}, 'by_tag_feed'),
    (r'^by-popularity.atom$', 'pathagar.books.views.most_downloaded',
     {'qtype': u'feed'}, 'most_downloaded_feed'),

    # Tag groups:
    (r'^tags/groups/(?P<group_slug>[-\w]+)/$', 'pathagar.books.views.tags',
     {}, 'tag_groups'),

    (r'^tags/groups/(?P<group_slug>[-\w]+).atom$', 'pathagar.books.views.tags',
     {'qtype': u'feed'}, 'tag_groups_feed'),

    # Tag list:
    (r'^tags/$', 'pathagar.books.views.tags', {}, 'tags'),
    (r'^tags.atom$', 'pathagar.books.views.tags',
     {'qtype': u'feed'}, 'tags_feed'),


    # Add, view, edit and remove books:
    (r'^book/add$', 'pathagar.books.views.add_book'),
    (r'^book/(?P<book_id>\d+)/view$', 'pathagar.books.views.book_detail'),
    (r'^book/(?P<book_id>\d+)/edit$', 'pathagar.books.views.edit_book'),
    (r'^book/(?P<book_id>\d+)/remove$', 'pathagar.books.views.remove_book'),
    (r'^book/(?P<book_id>\d+)/download$', 'pathagar.books.views.download_book'),

    # Comments
    (r'^comments/', include('django.contrib.comments.urls')),

    # Add language:
    (r'^add/dc_language|language/$', 'pathagar.books.views.add_language'),

    # Auth login and logout:
    (r'^accounts/login/$', 'django.contrib.auth.views.login'),
    (r'^accounts/logout/$', 'django.contrib.auth.views.logout'),

    # Admin:
    (r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    # Serve staticfiles
    from django.conf.urls.static import static
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

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
