# Copyright (C) 2010, One Laptop Per Child
# Copyright (C) 2010, Kushal Das
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

from cStringIO import StringIO

from django.core.urlresolvers import reverse

from atom import AtomFeed
import mimetypes

import datetime

ATTRS = {}
ATTRS[u'xmlns:dcterms'] = u'http://purl.org/dc/terms/'
ATTRS[u'xmlns:opds'] = u'http://opds-spec.org/'
ATTRS[u'xmlns:dc'] = u'http://purl.org/dc/elements/1.1/'
ATTRS[u'xmlns:opensearch'] = 'http://a9.com/-/spec/opensearch/1.1/'


def __get_mimetype(item):
    if item.mimetype is not None:
        return item.mimetype

    # The MIME Type was not stored in the database, try to guess it
    # from the filename:
    mimetype, encoding = mimetypes.guess_type(item.book_file.url)
    if mimetype is not None:
        return mimetype
    else:
        return 'Unknown'

def page_qstring(request, page_number=None):
    """
    Return the query string for the URL.
    
    If page_number is given, modify the query for that page.
    """
    qdict = dict(request.GET.items())
    if page_number is not None:
        qdict['page'] = str(page_number)
    
    if len(qdict) > 0:
        qstring = '?'+'&'.join(('%s=%s' % (k, v) for k, v in qdict.items()))
    else:
        qstring = ''
    
    return qstring

def generate_nav_catalog(subsections, is_root=False):
    links = []

    if is_root:
        links.append({'type': 'application/atom+xml',
                      'rel': 'self',
                      'href': reverse('books.views.root')})

    links.append({'title': 'Home', 'type': 'application/atom+xml',
                  'rel': 'start',
                  'href': reverse('books.views.root')})

    feed = AtomFeed(title = 'Pathagar Bookserver OPDS feed', \
        atom_id = 'pathagar:full-catalog', subtitle = \
        'OPDS catalog for the Pathagar book server', \
        extra_attrs = ATTRS, hide_generator=True, links=links)


    for subsec in subsections:
        feed.add_item(subsec['id'], subsec['title'],
                      subsec['updated'], links=subsec['links'])

    s = StringIO()
    feed.write(s, 'UTF-8')
    return s.getvalue()

def generate_root_catalog():
    subsections = [
        {'id': 'latest', 'title': 'Latest', 'updated': datetime.datetime.now(),
         'links': [{'rel': 'subsection', 'type': 'application/atom+xml', \
                    'href': reverse('latest_feed')}]},
        {'id': 'by-title', 'title': 'By Title', 'updated': datetime.datetime.now(),
         'links': [{'rel': 'subsection', 'type': 'application/atom+xml', \
                    'href': reverse('by_title_feed')}]},
        {'id': 'by-author', 'title': 'By Author', 'updated': datetime.datetime.now(),
         'links': [{'rel': 'subsection', 'type': 'application/atom+xml', \
                    'href': reverse('by_author_feed')}]},
        {'id': 'by-popularity', 'title': 'Most downloaded', 'updated': datetime.datetime.now(),
         'links': [{'rel': 'subsection', 'type': 'application/atom+xml', \
                    'href': reverse('most_downloaded_feed')}]},
        {'id': 'tags', 'title': 'Tags', 'updated': datetime.datetime.now(),
         'links': [{'rel': 'subsection', 'type': 'application/atom+xml', \
                    'href': reverse('tags_feed')}]},
        {'id': 'tag-groups', 'title': 'Tag groups', 'updated': datetime.datetime.now(),
         'links': [{'rel': 'subsection', 'type': 'application/atom+xml', \
                    'href': reverse('tags_listgroups')}]},
    ]
    return generate_nav_catalog(subsections)

def generate_tags_catalog(tags):
    def convert_tag(tag):
        return {'id': tag.name, 'title': tag.name,  'updated': datetime.datetime.now(),
                'links': [{'rel': 'subsection', 'type': 'application/atom+xml', \
                           'href': reverse('by_tag_feed', kwargs=dict(tag=tag.name))}]}

    tags_subsections = map(convert_tag, tags)
    return generate_nav_catalog(tags_subsections)

def generate_taggroups_catalog(tag_groups):
    def convert_group(group):
        return {'id': group.slug, 'title': group.name,  'updated': datetime.datetime.now(),
                'links': [{'rel': 'subsection', 'type': 'application/atom+xml', \
                           'href': reverse('tag_groups_feed', kwargs=dict(group_slug=group.slug))}]}

    tags_subsections = map(convert_group, tag_groups)
    return generate_nav_catalog(tags_subsections)


def generate_catalog(request, page_obj):
    links = []
    links.append({'title': 'Home', 'type': 'application/atom+xml',
                  'rel': 'start',
                  'href': reverse('books.views.root')})

    if page_obj.has_previous():
        previous_page = page_obj.previous_page_number()
        links.append({'title': 'Previous results', 'type': 'application/atom+xml',
                      'rel': 'previous',
                      'href': page_qstring(request, previous_page)})
    
    if page_obj.has_next():
        next_page = page_obj.next_page_number()
        links.append({'title': 'Next results', 'type': 'application/atom+xml',
                      'rel': 'next',
                      'href': page_qstring(request, next_page)})
    
    feed = AtomFeed(title = 'Pathagar Bookserver OPDS feed', \
        atom_id = 'pathagar:full-catalog', subtitle = \
        'OPDS catalog for the Pathagar book server', \
        extra_attrs = ATTRS, hide_generator=True, links=links)

    for book in page_obj.object_list:
        if book.cover_img:
            linklist = [{'rel': \
                    'http://opds-spec.org/acquisition', 'href': \
                    reverse('books.views.download_book',
                            kwargs=dict(book_id=book.pk)),
                    'type': __get_mimetype(book)}, {'rel': \
                    'http://opds-spec.org/cover', 'href': \
                    book.cover_img.url }]
        else:
           linklist = [{'rel': \
                    'http://opds-spec.org/acquisition', 'href': \
                    reverse('books.views.download_book',
                            kwargs=dict(book_id=book.pk)),
                    'type': __get_mimetype(book)}]
        
        add_kwargs = {
            'content': book.a_summary,
            'links': linklist,
            'authors': [{'name' : book.a_author}],
            'dc_publisher': book.dc_publisher,
            'dc_issued': book.dc_issued,
            'dc_identifier': book.dc_identifier,
        }
           
        if book.dc_language is not None:
            add_kwargs['dc_language'] = book.dc_language.code

        feed.add_item(book.a_id, book.a_title, book.a_updated, **add_kwargs)

    s = StringIO()
    feed.write(s, 'UTF-8')
    return s.getvalue()
