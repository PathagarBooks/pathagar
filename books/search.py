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
from models import Book


def simple_search(queryset, searchterms,
                  search_title=False, search_author=False):
    q_objects = []
    results = queryset
    
    subterms = searchterms.split(' ')
    for subterm in subterms:
        word = subterm
        if search_title:
            q_objects.append(Q(a_title__icontains = word))
        if search_author:
            q_objects.append(Q(a_author__icontains = word))
    
    for q_object in q_objects:
        results = results.filter(q_object)
    return results

def advanced_search(queryset, searchterms):
    """
    Does an advanced search in several fields of the books.
    """
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
