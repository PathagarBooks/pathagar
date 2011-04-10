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

import os
import csv

from books.models import Book
import settings

class Command(BaseCommand):
    help = "Adds a book collection (via a CSV file)"
    args = 'Absolute path to CSV file'

    def handle(self, csvpath='', *args, **options):
        if not os.path.exists(csvpath):
            raise CommandError("%r is not a valid path" % csvpath)

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


