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

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404
from django.core.files.base import ContentFile
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.views.generic.simple import redirect_to
from django.views.generic.list_detail import object_list, object_detail
from django.views.generic.create_update import create_object, update_object, \
  delete_object
from django.template import RequestContext

from django.conf import settings

from tagging.utils import get_tag
from tagging.models import TaggedItem

from search import simple_search, advanced_search
from forms import BookForm, AddLanguageForm
from langlist import langs as LANG_CHOICES
from models import *
from popuphandler import handlePopAdd
from opds import page_qstring, generate_catalog

@login_required
def add_language(request):
    return handlePopAdd(request, AddLanguageForm, 'language')

@login_required
def add_book(request):
    extra_context = {'action': 'add'}
    return create_object(
        request,
        form_class = BookForm,
        extra_context = extra_context,
    )

@login_required
def edit_book(request, book_id):
    extra_context = {'action': 'edit'}
    return update_object(
        request,
        form_class = BookForm,
        object_id = book_id,
        template_object_name = 'book',
        extra_context = extra_context,
    )

@login_required
def remove_book(request, book_id):
    return delete_object(
        request,
        model = Book,
        object_id = book_id,
        template_object_name = 'book',
        post_delete_redirect = '/',
    )

def _book_list(request, queryset, qtype=None, list_by='latest', **kwargs):
    q = request.GET.get('q')
    search_all = request.GET.get('search-all') == 'on'
    search_title = request.GET.get('search-title') == 'on'
    search_author = request.GET.get('search-author') == 'on'
    
    # If no search options are specified, assumes search all, the
    # advanced search will be used:
    if not search_all and not search_title and not search_author:
        search_all = True
    
    # If search queried, modify the queryset with the result of the
    # search:
    if q is not None:
        if search_all:
            queryset = advanced_search(queryset, q)
        else:
            queryset = simple_search(queryset, q,
                                     search_title, search_author)
    
    all_books = Book.objects.all()
    
    paginator = Paginator(queryset, settings.ITEMS_PER_PAGE)
    page = int(request.GET.get('page', '1'))
    
    try:
        page_obj = paginator.page(page)
    except (EmptyPage, InvalidPage):
        page_obj = paginator.page(paginator.num_pages)
    
    # Build the query string:
    qstring = page_qstring(request)
    
    # Return OPDS Atom Feed:
    if qtype == 'feed':
        catalog = generate_catalog(request, page_obj)
        return HttpResponse(catalog, mimetype='application/atom+xml')
    
    # Return HTML page:
    extra_context = dict(kwargs)
    extra_context.update({
        'book_list': page_obj.object_list,
        'total_books': len(all_books), 'q': q,
        'paginator': paginator,
        'page_obj': page_obj,
        'search_title': search_title,
        'search_author': search_author, 'list_by': list_by,
        'qstring': qstring,
    })
    return render_to_response(
        'books/book_list.html',
        extra_context,
        context_instance = RequestContext(request),
    )

def latest(request, qtype=None):
    queryset = Book.objects.all()
    return _book_list(request, queryset, qtype, list_by='latest')

def by_title(request, qtype=None):
    queryset = Book.objects.all().order_by('a_title')
    return _book_list(request, queryset, qtype, list_by='by-title')

def by_author(request, qtype=None):
    queryset = Book.objects.all().order_by('a_author')
    return _book_list(request, queryset, qtype, list_by='by-author')

def by_tag(request, tag, qtype=None):
    tag_instance = get_tag(tag)
    if tag_instance is None:
        raise Http404()
    queryset = Book.objects.all()
    queryset = TaggedItem.objects.get_by_model(queryset, tag_instance)
    return _book_list(request, queryset, qtype, list_by='by-tag',
                      tag=tag_instance)

def book_detail(request, book_id):
    return object_detail(
        request,
        queryset = Book.objects.all(),
        object_id = book_id,
        template_object_name = 'book',
    )
