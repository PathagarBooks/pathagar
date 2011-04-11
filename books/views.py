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

from catalog import get_catalog
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


def page(request):
    """
    books = Book.objects.all().order_by('a_title')
    paginator = Paginator(books, 2)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    # If page request (9999) is out of range, deliver last page of results.
    try:
        books = paginator.page(page)
    except (EmptyPage, InvalidPage):
        books = paginator.page(paginator.num_pages)
    """
    all_books = Book.objects.all()
    books, q = get_catalog(request,'html')
    return render_to_response('index.html', {'books': books, 'q':q, 'total_books':len(all_books)})

def book_details(request, book_id):
    return object_detail(
        request,
        queryset = Book.objects.all(),
        object_id = book_id,
        template_object_name = 'book',
    )
