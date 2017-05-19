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

import os

from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.http import Http404
from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.views.generic.list_detail import object_detail
from django.views.generic.create_update import create_object, update_object, \
  delete_object
from django.template import RequestContext, resolve_variable

from app_settings import BOOKS_PER_PAGE, AUTHORS_PER_PAGE
from django.conf import settings

# OLD ---------------
from tagging.models import Tag
# --------------- OLD
from taggit.models import Tag as tTag

from sendfile import sendfile

from search import simple_search, advanced_search
from forms import BookForm, AddLanguageForm
from models import TagGroup, Book, Author
from popuphandler import handlePopAdd
from opds import page_qstring
from opds import generate_catalog
from opds import generate_root_catalog
from opds import generate_tags_catalog
from opds import generate_taggroups_catalog

from pathagar.books.app_settings import BOOK_PUBLISHED


@login_required
def add_language(request):
    return handlePopAdd(request, AddLanguageForm, 'language')

def add_book(request):
    context_instance = RequestContext(request)
    user = resolve_variable('user', context_instance)
    if not settings.ALLOW_PUBLIC_ADD_BOOKS and not user.is_authenticated():
        next = reverse('pathagar.books.views.add_book')
        return redirect('/accounts/login/?next=%s' % next)

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

def book_detail(request, book_id):
    return object_detail(
        request,
        queryset = Book.objects.all(),
        object_id = book_id,
        template_object_name = 'book',
        extra_context = {'allow_user_comments': settings.ALLOW_USER_COMMENTS}
    )

def download_book(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    filename = os.path.join(settings.MEDIA_ROOT, book.book_file.name)

    # TODO, currently the downloads counter is incremented when the
    # download is requested, without knowing if the file sending was
    # successfull:
    book.downloads += 1
    book.save()
    return sendfile(request, filename, attachment=True)

def tags(request, qtype=None, group_slug=None):
    context = {'list_by': 'by-tag'}

    if group_slug is not None:
        tag_group = get_object_or_404(TagGroup, slug=group_slug)
        context.update({'tag_group': tag_group})
        context.update({'tag_list': Tag.objects.get_for_object(tag_group)})
    else:
        context.update({'tag_list': tTag.objects.all()})

    tag_groups = TagGroup.objects.all()
    context.update({'tag_group_list': tag_groups})


    # Return OPDS Atom Feed:
    if qtype == 'feed':
        catalog = generate_tags_catalog(context['tag_list'])
        return HttpResponse(catalog, mimetype='application/atom+xml')

    # Return HTML page:
    return render_to_response(
        'books/tag_list.html', context,
        context_instance = RequestContext(request),
    )

def tags_listgroups(request):
    tag_groups = TagGroup.objects.all()
    catalog = generate_taggroups_catalog(tag_groups)
    return HttpResponse(catalog, mimetype='application/atom+xml')

def _book_list(request, queryset, qtype=None, list_by='latest', **kwargs):
    """
    Filter the books, paginate the result, and return either a HTML
    book list, or a atom+xml OPDS catalog.

    """
    q = request.GET.get('q')
    search_all = request.GET.get('search-all') == 'on'
    search_title = request.GET.get('search-title') == 'on'
    search_author = request.GET.get('search-author') == 'on'

    context_instance = RequestContext(request)
    user = resolve_variable('user', context_instance)
    if not user.is_authenticated():
        queryset = queryset.filter(a_status = BOOK_PUBLISHED)

    published_books_count = Book.objects.filter(a_status = BOOK_PUBLISHED).count()
    unpublished_books_count = Book.objects.exclude(a_status = BOOK_PUBLISHED).count()

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

    paginator = Paginator(queryset, BOOKS_PER_PAGE)
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
        'published_books': published_books_count,
        'unpublished_books': unpublished_books_count,
        'q': q,
        'paginator': paginator,
        'page_obj': page_obj,
        'search_title': search_title,
        'search_author': search_author, 'list_by': list_by,
        'qstring': qstring,
        'allow_public_add_book': settings.ALLOW_PUBLIC_ADD_BOOKS
    })
    return render_to_response(
        'books/book_list.html',
        extra_context,
        context_instance = RequestContext(request),
    )

def _author_list(request, queryset, qtype=None, list_by='latest', **kwargs):
    """
    Filter the books, paginate the result, and return either a HTML
    book list, or a atom+xml OPDS catalog.

    """
    q = request.GET.get('q')
    # search_all = request.GET.get('search-all') == 'on'
    # search_title = request.GET.get('search-title') == 'on'
    search_author = request.GET.get('search-author') == 'on'

    # context_instance = RequestContext(request)
    # user = resolve_variable('user', context_instance)
    # if not user.is_authenticated():
    #     queryset = queryset.filter(a_status = BOOK_PUBLISHED)

    # published_books_count = Book.objects.filter(a_status = BOOK_PUBLISHED).count()
    # unpublished_books_count = Book.objects.exclude(a_status = BOOK_PUBLISHED).count()

    # If no search options are specified, assumes search all, the
    # advanced search will be used:
    # if not search_all and not search_title and not search_author:
    #     search_all = True

    # FIXME
    # If search queried, modify the queryset with the result of the
    # search:
    # if q is not None:
    #     if search_all:
    #         queryset = advanced_search(queryset, q)
    #     else:
    #         queryset = simple_search(queryset, q,
    #                                  search_title, search_author)

    paginator = Paginator(queryset, BOOKS_PER_PAGE)
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
        'author_list': page_obj.object_list,
        # 'published_books': published_books_count,
        # 'unpublished_books': unpublished_books_count,
        'q': q,
        'paginator': paginator,
        'page_obj': page_obj,
        # 'search_title': search_title,
        'search_author': search_author,
        'list_by': list_by,
        'qstring': qstring,
        # 'allow_public_add_book': settings.ALLOW_PUBLIC_ADD_BOOKS
    })
    return render_to_response(
        'authors/author_list.html',
        extra_context,
        context_instance = RequestContext(request),
    )

def home(request):
    return redirect('latest')

def root(request, qtype=None):
    """Return the root catalog for navigation"""
    root_catalog = generate_root_catalog()
    return HttpResponse(root_catalog, mimetype='application/atom+xml')

def latest(request, qtype=None):
    queryset = Book.objects.all()
    return _book_list(request, queryset, qtype, list_by='latest')

def by_title(request, qtype=None):
    queryset = Book.objects.all().order_by('a_title')
    return _book_list(request, queryset, qtype, list_by='by-title')

def by_author(request, qtype=None):
    #queryset = Book.objects.all().order_by('a_author')
    #return _book_list(request, queryset, qtype, list_by='by-author')
    queryset = Author.objects.all().order_by('a_author')
    print("stuff")
    return _author_list(request, queryset, qtype, list_by='by-author')

def by_tag(request, tag, qtype=None):
    """ displays a book list by the tag argument """
    # get the Tag object
    tag_instance = tTag.objects.get(name=tag) # TODO replace as Tag when django-tagging is removed

    # if the tag does not exist, return 404
    if tag_instance is None:
        raise Http404()

    # Get a list of books that have the requested tag
    queryset = Book.objects.filter(tags=tag_instance)
    return _book_list(request, queryset, qtype, list_by='by-tag',
                      tag=tag_instance)

def most_downloaded(request, qtype=None):
    queryset = Book.objects.all().order_by('-downloads')
    return _book_list(request, queryset, qtype, list_by='most-downloaded')

