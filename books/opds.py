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


from models import Book
from atom import AtomFeed

import logging


def __get_mimetype(item):
    if item.file.url.endswith('pdf'):
        return 'application/pdf'
    elif item.file.url.endswith('epub'):
        return 'application/epub+zip'
    else:
        return 'Unknown'


def generate_catalog(books,q=None):
    attrs = {}
    attrs[u'xmlns:dcterms'] = u'http://purl.org/dc/terms/'
    attrs[u'xmlns:opds'] = u'http://opds-spec.org/'
    attrs[u'xmlns:dc'] = u'http://purl.org/dc/elements/1.1/'
    attrs[u'xmlns:opensearch'] = 'http://a9.com/-/spec/opensearch/1.1/'

    links = []

    if books.has_previous():
        if q:
            links.append({'title':'Previous results','type':'application/atom+xml',\
            'rel':'previous','href':'?page=' + str(books.previous_page_number()) + '&q=' + q })
        else:
            links.append({'title':'Previous results','type':'application/atom+xml',\
            'rel':'previous','href':'?page=' + str(books.previous_page_number())})


    if books.has_next():
        if q:
            links.append({'title':'Next results','type':'application/atom+xml',\
            'rel':'next','href':'?page=' + str(books.next_page_number()) + '&q=' + q })
        else:
            links.append({'title':'Next results','type':'application/atom+xml',\
            'rel':'next','href':'?page=' + str(books.next_page_number())})




    feed = AtomFeed(title = 'Pathagar Bookserver OPDS feed', \
        atom_id = 'pathagar:full-catalog', subtitle = \
        'OPDS catalog for the Pathagar book server', \
        extra_attrs = attrs, hide_generator=True, links=links)


    for book in books.object_list:
        feed.add_item(book.a_id, book.a_title, book.a_updated, \
            content=book.a_summary, links = [{'rel': \
            'http://opds-spec.org/acquisition', 'href': \
            book.file.url, 'type': __get_mimetype(book)}], \
            authors = [{'name' : book.a_author}], dc_language=book.dc_language, \
            dc_publisher=book.dc_publisher, dc_issued=book.dc_issued, \
            dc_identifier=book.dc_identifier)

    s = StringIO()
    feed.write(s, 'UTF-8')
    return s.getvalue()
