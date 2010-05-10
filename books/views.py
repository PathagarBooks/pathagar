from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.core.files.base import ContentFile

from opds import get_catalog
from forms import AddBookForm
from models import *

def catalogs(request):
    return HttpResponse(get_catalog(request), mimetype='application/atom+xml')


def add_book(request):
    book = None
    if request.method == 'POST':
        form = AddBookForm(request.POST,request.FILES)
        title = form['a_title']
        author = form['a_author']
        if not form.is_valid():
            form = AddBookForm()
            return render_to_response('addbook.html', {'form': form})

        book = form.save()


    form = AddBookForm()
    if book:
        return render_to_response('addbook.html', {'form': form,'book':book.id})
    return render_to_response('addbook.html', {'form': form})

