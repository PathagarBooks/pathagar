from django.core.management.base import BaseCommand, CommandError
from django.core.files.storage import default_storage
from django.core.files import File
from django.db.utils import IntegrityError

import os

from books.models import *
from books.epub import *
from books.langlist import *

import settings

import sys

def get_epubs(path):
    """Returns a list of EPUB(s)"""
    epub_list = []

    for root, dirs, files in os.walk(path):
        for name in files:
            if name.lower().endswith('.epub'):
                epub_list.append(os.path.join(root,name))

    return epub_list


class Command(BaseCommand):
    help = "Adds a book collection (via a directory containing EPUB file(s))"
    args = 'Absolute path to directory of EPUB files'

    def handle(self, dirpath='', *args, **options):
        if not os.path.exists(dirpath):
            raise CommandError("%r is not a valid path" % dirpath)


        if os.path.isdir(dirpath):
            names = get_epubs(dirpath)
            for name in names:
                info = None
                try:
                    e = Epub(name)
                    info = e.get_info()
                except:
                    print "%s is not a valid epub file" % name
                    continue
                lang = Language.objects.filter(code=info.language)
                if not lang:
                    for data in langs:
                        if data[0] == info.language:
                            lang = Language()
                            lang.label = data[1]
                            lang.save()
                            break
                else:
                    lang = lang[0]

                #XXX: Hacks below
                if not info.title:
                    info.title = ''
                if not info.summary:
                    info.summary = ''
                if not info.creator:
                    info.creator = ''
                if not info.rights:
                    info.rights = ''

                f = open(name)
                pub_status = Status.objects.get(status='Published')
                book = Book(book_file=File(f), a_title = info.title, \
                        a_author = info.creator, a_summary = info.summary, \
                        a_rights = info.rights, dc_identifier = info.identifier['value'].strip('urn:uuid:'), \
                        dc_issued = info.date,
                        a_status = pub_status)

                try:
                    book.save()
                # FIXME: Find a better way to do this.
                except IntegrityError as e:
                    if str(e) == "column file_sha256sum is not unique":
                        print "The book (", book.book_file, ") was not saved because the file already exsists in the database."
                    else:
                        raise CommandError('Error adding file %s: %s' % (book.book_file, sys.exc_info()[1]))
                except:
                    raise CommandError('Error adding file %s: %s' % (book.book_file, sys.exc_info()[1]))

