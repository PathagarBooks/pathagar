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
            book = Book(file = File(f), a_title = title, a_author = author, a_summary = summary)
            book.save()


