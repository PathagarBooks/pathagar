import os

from django.conf.urls import include, url

from django.conf import settings
from books.app_settings import BOOKS_STATICS_VIA_DJANGO

from books import views


urlpatterns = [

    # Book list:
    url(r'^$', views.home,
     kwargs={}, name='home'),
    url(r'^latest/$', views.latest,
     {}, name='latest'),
    url(r'^by-title/$', views.by_title,
     {}, 'by_title'),
    url(r'^by-author/$', views.by_author,
     {}, 'by_author'),
    url(r'^by-author/(?P<author_id>\d+)/$', views.by_title,
     {}, 'books_by_author'),
    url(r'^tags/(?P<tag>.+)/$', views.by_tag,
     {}, 'by_tag'),
    url(r'^by-popularity/$', views.most_downloaded,
     {}, 'most_downloaded'),

    # Tag groups:
    url(r'^tags/groups.atom$', views.tags_listgroups,
     {}, 'tags_listgroups'),

    # Book list Atom:
    url(r'^catalog.atom$', views.root,
     {'qtype': u'feed'}, 'root_feed'),
    url(r'^latest.atom$', views.latest,
     {'qtype': u'feed'}, 'latest_feed'),
    url(r'^by-title.atom$', views.by_title,
     {'qtype': u'feed'}, 'by_title_feed'),
    url(r'^by-author.atom$', views.by_author,
     {'qtype': u'feed'}, 'by_author_feed'),
    url(r'^by-author/(?P<author_id>\d+).atom$', views.by_title,
     {'qtype': u'feed'}, 'by_title_author_feed'),
    url(r'^tags/(?P<tag>.+).atom$', views.by_tag,
     {'qtype': u'feed'}, 'by_tag_feed'),
    url(r'^by-popularity.atom$', views.most_downloaded,
     {'qtype': u'feed'}, 'most_downloaded_feed'),

    # Tag groups:
    url(r'^tags/groups/(?P<group_slug>[-\w]+)/$', views.tags,
     {}, 'tag_groups'),

    url(r'^tags/groups/(?P<group_slug>[-\w]+).atom$', views.tags,
     {'qtype': u'feed'}, 'tag_groups_feed'),

    # Tag list:
    url(r'^tags/$', views.tags, {}, 'tags'),
    url(r'^tags.atom$', views.tags,
     {'qtype': u'feed'}, 'tags_feed'),

    # Add, view, edit and remove books:
    url(r'^book/add$', views.BookAddView.as_view(), name='book_add'),
    url(r'^book/(?P<pk>\d+)/view$', views.BookDetailView.as_view(), name='book_detail'),
    url(r'^book/(?P<pk>\d+)/edit$', views.BookEditView.as_view(), name='book_edit'),
    url(r'^book/(?P<pk>\d+)/remove$', views.BookDeleteView.as_view(), name='book_remove'),
    url(r'^book/(?P<book_id>\d+)/download$', views.download_book, name='book_download'),

    # Comments
    # FIXME (r'^comments/', include('django.contrib.comments.urls')),

    # Add language:
    url(r'^add/dc_language|language/$', views.add_language),
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
