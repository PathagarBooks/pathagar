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

from django.conf import settings

from catalog import get_catalog, search_books
from forms import BookForm, AddLanguageForm
from langlist import langs as LANG_CHOICES
from models import *
from popuphandler import handlePopAdd

def catalogs(request):
    return HttpResponse(get_catalog(request), mimetype='application/atom+xml')

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

def _book_list(request, queryset, list_by='latest'):
    print request.GET.keys()
    q = request.GET.get('q')
    if q is not None:
        queryset = search_books(queryset, q)
    
    all_books = Book.objects.all()
    extra_context = {'total_books': len(all_books), 'q': q,
                      'list_by': list_by}
    return object_list(
        request,
        queryset = queryset,
        paginate_by = settings.ITEMS_PER_PAGE,
        template_object_name = 'book',
        extra_context = extra_context,
    )

def book_list(request):
    queryset = Book.objects.all()
    return _book_list(request, queryset, list_by='latest')

def by_title(request):
    queryset = Book.objects.all().order_by('a_title')
    return _book_list(request, queryset, list_by='by-title')

def by_author(request):
    queryset = Book.objects.all().order_by('a_author')
    return _book_list(request, queryset, list_by='by-author')

def book_detail(request, book_id):
    return object_detail(
        request,
        queryset = Book.objects.all(),
        object_id = book_id,
        template_object_name = 'book',
    )
