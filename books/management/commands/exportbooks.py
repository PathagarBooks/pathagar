# Copyright (C) 2010, One Laptop Per Child
# Copyright (C) 2017, Michael Bonfils
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

# TODO pylint-django is creating no-member false positives here
# pylint: disable=no-member

from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ValidationError
from django.core.files import File

from django.db import transaction
from django.db.utils import IntegrityError

import csv
import json
import logging
import os
import shutil
import sys
from optparse import make_option

from books.models import Book, Status

logger = logging.getLogger(__name__)
logging.basicConfig()
logger.setLevel(logging.DEBUG)

class Command(BaseCommand):
    help = "Dump collection in directory (CSV + books)"
    args = 'Directory Path'


    def _handle_csv(self, csvpath):
        """
        Export books into directory with CSV catalog
        WARN: does not handle tags

        """

        csvfile = open(csvpath + "/catalog.csv", "w")
        writer = csv.DictWriter(csvfile, ['filename', 'title', 'author', 'summary'])
        writer.writeheader()

        for book in Book.objects.all():
            shutil.copy(book.book_file.file.name, csvpath)

            entry = {'filename': os.path.basename(book.book_file.name).encode('utf-8'),
                'a_title': book.a_title.encode('utf-8'),
                'a_author': book.a_author.a_author.encode('utf-8'),
                'a_summary': book.a_summary.encode('utf-8')}
            writer.writerow(entry)
        csvfile.close()


    def handle(self, filepath='', *args, **options):
        if filepath == '' or not os.path.exists(filepath):
            raise CommandError("%r is not a valid path" % filepath)
        filepath = os.path.abspath(filepath)

        self._handle_csv(filepath)
