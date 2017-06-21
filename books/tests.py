from django.test import TestCase
from books.epub import Epub

class EpubTest(TestCase):
    def test_simple_import(self):
        epub = Epub("examples/The Dunwich Horror.epub")
        info = epub.get_info()
        self.assertEqual(info.title, "The Dunwich Horror")
        self.assertEqual(info.creator, "H. P. Lovecraft")
        epub.close()
