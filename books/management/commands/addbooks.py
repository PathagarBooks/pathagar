# Copyright (C) 2010, One Laptop Per Child
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

from django.core.management.base import BaseCommand, CommandError
from django.core.files.storage import default_storage
from django.core.files import File

from django.db.utils import IntegrityError

import sys
import os
import csv
import json
from optparse import make_option

from books.models import Book, Status
import settings

class Command(BaseCommand):
    help = "Adds a book collection (via a CSV file)"
    args = 'Absolute path to CSV file'

    option_list = BaseCommand.option_list + (
        make_option('--json',
            action='store_true',
            dest='is_json_format',
            default=False,
            help='The file is in JSON format'),
        )

    def _handle_csv(self, csvpath):
        """
        Store books from a file in CSV format.
        WARN: does not handle tags

        """

        csvfile = open(csvpath)
        dialect = csv.Sniffer().sniff(csvfile.read(1024))
        csvfile.seek(0)
        reader = csv.reader(csvfile, dialect)

        #TODO: Figure out if this is a valid CSV file

        for row in reader:
            path = row[0]
            title = row[1]
            author = row[2]
            summary =  row[3]

            f = open(path)
            book = Book(book_file = File(f), a_title = title, a_author = author, a_summary = summary)
            book.save()

    def _handle_json(self, jsonpath):
        """
        Store books from a file in JSON format.

        """
        jsonfile = open(jsonpath)
        data_list = json.loads(jsonfile.read())
        for d in data_list:
            # Get a Django File from the given path:
            f = open(d['book_path'])
            d['book_file'] = File(f)
            del d['book_path']

            if d.has_key('cover_path'):
                f_cover = open(d['cover_path'])
                d['cover_img'] = File(f_cover)
                del d['cover_path']


            if d.has_key('a_status'):
                d['a_status'] = Status.objects.get(status = d['a_status'])

            tags = d['tags']
            del d['tags']

            book = Book(**d)
            try:
                book.save() # must save item to generate Book.id before creating tags
                [book.tags.add(tag) for tag in tags]
                book.save() # save again after tags are generated
            except IntegrityError as e:
                if str(e) == "column file_sha256sum is not unique":
                    print "The book (", d['book_file'], ") was not saved because the file already exsists in the database."
                else:
                    raise CommandError('Error adding file %s: %s' % (d['book_file'], sys.exc_info()[1]))

    def handle(self, filepath='', *args, **options):
        if not os.path.exists(filepath):
            raise CommandError("%r is not a valid path" % filepath)

        if options['is_json_format']:
            self._handle_json(filepath)
        else:
            self._handle_csv(filepath)


