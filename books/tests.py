from django.test import TestCase
from django.core.management import call_command, CommandError

from books.epub import Epub
from books.models import Book, Author


class EpubTest(TestCase):
    def test_simple_import(self):
        epub = Epub("examples/The Dunwich Horror.epub")
        info = epub.get_info()
        self.assertEqual(info.title, "The Dunwich Horror")
        self.assertEqual(info.creator, "H. P. Lovecraft")
        epub.close()


class AddEpubTest(TestCase):
    def test_01_import_commandline(self):
        nb_book = len(Book.objects.all())
        self.assertEqual(nb_book, 0)

        args = ["examples/"]
        opts = {}
        call_command('addepub', *args, **opts)

        nb_book = len(Book.objects.all())
        self.assertEqual(nb_book, 1)

        book = Book.objects.get(pk=1)
        self.assertEqual(str(book.a_author), "H. P. Lovecraft")
        self.assertEqual(str(book.a_title), "The Dunwich Horror")

    def test_02_import_duplicated(self):
        # try to import duplicated epub
        args = ["examples/"]
        opts = {}
        call_command('addepub', *args, **opts)
        self.assertRaises(CommandError, call_command,
            ('addepub'), opts)
