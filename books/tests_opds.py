from lxml import etree

from django.test import TestCase, Client
from django.core.management import call_command, CommandError
from django.urls import reverse_lazy

from books.epub import Epub
from books.models import Book, Author


class OpdsTest(TestCase):
    def setUp(self):
        nb_book = len(Book.objects.all())
        self.assertEqual(nb_book, 0)

        args = ["examples/"]
        opts = {}
        call_command('addepub', *args, **opts)

    def test_01_full_import_commandline(self):
        c = Client()

        for opds in (u'latest_feed', u'root_feed', u'by_author_feed', u'by_title_feed', u'most_downloaded_feed'):
            d = c.get(reverse_lazy(opds))
            d = d.content
            parser = etree.fromstring(d)

        # by author
        d = c.get(reverse_lazy('by_title_author_feed',
            kwargs=dict(author_id=1)))
        d = d.content
        parser = etree.fromstring(d)
