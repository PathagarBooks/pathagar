from cStringIO import StringIO

from django.db.models import Q

from models import Book
from atom import AtomFeed

import logging

#XXX: Implement pagination

def __get_mimetype(item):
    if item.file.url.endswith('pdf'):
        return 'application/pdf'
    else:
        return 'Unknown'

def get_catalog(request):
    if not len(request.GET):
        return get_full_catalog()
    else:
        q_objects = []
        results = Book.objects.all()
        searchterms = request.GET['q']
        subterms = searchterms.split('AND')
        for subterm in subterms:
            if ':' in subterm:
                key, word = subterm.split(':')
                key = key.strip()
                if key == 'title':
                    q_objects.append(Q(a_title__icontains = word))
                if key == 'author':
                    q_objects.append(Q(a_author__icontains = word))
                if key == 'publisher':
                    q_objects.append(Q(dc_publisher__icontains = word))
                if key == 'identifier':
                    q_objects.append(Q(dc_identifier__icontains = word))
                if key == 'summary':
                    q_objects.append(Q(a_summary__icontains = word))
            else:
                word = subterm
                try:
                    results = results.get(Q(a_title__icontains = word) | \
                        Q(a_author__icontains = word) | \
                        Q(dc_publisher__icontains = word) | \
                        Q(dc_identifier__icontains = word) | \
                        Q(a_summary__icontains = word))
                except Book.DoesNotExist:
                    results = Book.objects.none()

        for q_object in q_objects:
            results = results.filter(q_object)

        return generate_catalog(results)


def get_full_catalog():
    books = Book.objects.order_by('a_title')
    return generate_catalog(books)


def generate_catalog(books):
    attrs = {}
    attrs[u'xmlns:dcterms'] = u'http://purl.org/dc/terms/'
    attrs[u'xmlns:opds'] = u'http://opds-spec.org/'
    attrs[u'xmlns:dc'] = u'http://purl.org/dc/elements/1.1/'
    attrs[u'xmlns:opensearch'] = 'http://a9.com/-/spec/opensearch/1.1/'

    feed = AtomFeed(title = 'Pathagar Bookserver OPDS feed', \
        atom_id = 'pathagar:full-catalog', subtitle = \
        'OPDS catalog for the Pathagar book server', \
        extra_attrs = attrs, hide_generator=True)

    if isinstance(books, Book):
        books = [books] ###FIXME 

    for book in books:
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
