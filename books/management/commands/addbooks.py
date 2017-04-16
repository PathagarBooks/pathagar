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
from django.core.exceptions import ValidationError
from django.core.files import File

from django.db import transaction
from django.db.utils import IntegrityError

import csv
import json
import logging
import os
import sys
from optparse import make_option

from books.models import Book, Status

logger = logging.getLogger(__name__)
logging.basicConfig()
logger.setLevel(logging.DEBUG)

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

        # TODO: Figure out if this is a valid CSV file

        status_published = Status.objects.get(status='Published')

        for row in reader:
            path = row[0]
            title = row[1]
            author = row[2]
            summary = row[3]

            if os.path.exists(path):
                f = open(path)
                book = Book(book_file=File(f), a_title=title, a_author=author,
                            a_summary=summary, a_status=status_published)
                try:
                    book.save()
                except:
                    print "EXCEPTION SAVING FILE '%s': %s" % (
                        path, sys.exc_info()[0])
            else:
                print "FILE NOT FOUND '%s'" % path

    def _handle_json(self, jsonpath):
        """
        Store books from a file in JSON format.

        """
        jsonfile = open(jsonpath)
        data_list = json.loads(jsonfile.read())

        status_published = Status.objects.get(status='Published')
        stats = dict(total=0, errors=0, skipped=0, imported=0)

        for d in data_list:
            stats['total'] += 1
            logger.debug('read item %s' % json.dumps(d))

            # Skip unless there is book content
            if 'book_path' not in d:
                stats['skipped'] += 1
                continue

            # Skip unless there is book content
            if not os.path.exists(d['book_path']):
                stats['skipped'] += 1
                continue

            # Get a Django File from the given path:
            f = open(d['book_path'])
            d['book_file'] = File(f)
            del d['book_path']

            if 'cover_path' in d:
                f_cover = open(d['cover_path'])
                d['cover_img'] = File(f_cover)
                del d['cover_path']

            if 'a_status' in d:
                d['a_status'] = Status.objects.get(status=d['a_status'])
            else:
                d['a_status'] = status_published

            tags = d.get('tags', [])
            if 'tags' in d:
                del d['tags']

            book = Book(**d)
            try:
                book.validate_unique() # Throws ValidationError if not unique

                with transaction.commit_on_success():
                    book.save() # must save item to generate Book.id before creating tags
                    [book.tags.add(tag) for tag in tags if tag]
                    book.save()  # save again after tags are generated
                    stats['imported'] += 1
            except ValidationError as e:
                stats['skipped'] += 1
                logger.info('Book already imported, skipping title="%s"' % book.a_title)
            except Exception as e:
                stats['errors'] += 1
                # Likely a bug
                logger.warn('Error adding book title="%s": %s' % (
                    book.a_title, e))

        logger.info("addbooks complete total=%(total)d imported=%(imported)d skipped=%(skipped)d errors=%(errors)d" % stats)


    def handle(self, filepath='', *args, **options):
        if not os.path.exists(filepath):
            raise CommandError("%r is not a valid path" % filepath)

        if options['is_json_format']:
            self._handle_json(filepath)
        else:
            self._handle_csv(filepath)
