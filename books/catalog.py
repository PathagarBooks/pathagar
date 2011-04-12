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

from django.db.models import Q
from django.core.paginator import Paginator, InvalidPage, EmptyPage

from models import Book
from opds import generate_catalog

from django.conf import settings

def search_books(queryset, searchterms):
    q_objects = []
    results = queryset
    
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
                results = results.filter(Q(a_title__icontains = word) | \
                    Q(a_author__icontains = word) | \
                    Q(dc_publisher__icontains = word) | \
                    Q(dc_identifier__icontains = word) | \
                    Q(a_summary__icontains = word))
            except Book.DoesNotExist:
                results = Book.objects.none()

    for q_object in q_objects:
        results = results.filter(q_object)
    return results

def get_catalog(request, qtype='feed'):
    results = Book.objects.all()
    q = request.GET.get('q')
    if q is not None:
        results = search_books(results, q)
    
    paginator = Paginator(results, settings.ITEMS_PER_PAGE)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    
    try:
        books = paginator.page(page)
    except (EmptyPage, InvalidPage):
        books = paginator.page(paginator.num_pages)
    
    if qtype == 'feed':
        return generate_catalog(books, q)
    
    return (books, q)

