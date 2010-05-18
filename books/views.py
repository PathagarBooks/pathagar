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
from django.core.files.base import ContentFile
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, InvalidPage, EmptyPage

from catalog import get_catalog
from forms import AddBookForm, AddLanguageForm
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
    book = None
    if request.method == 'POST':
        form = AddBookForm(request.POST, request.FILES)
        title = form['a_title']
        author = form['a_author']
        if not form.is_valid():
            form = AddBookForm()
            return render_to_response('addbook.html', {'form': form})

        book = form.save()


    form = AddBookForm()
    if book:
        return render_to_response('addbook.html', {'form': form, 'book':book.id})
    return render_to_response('addbook.html', {'form': form})

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


