from django.test import TestCase
from books.models import Book, Status

class LoginRequiredPagesTest(TestCase):
    def setUp(self):
        #TODO move this into a test fixture
        published = Status(status="Published")
        published.save()

        book = Book(
            a_title="Red Fish Two Fish One Fish Blue Fish",
            a_author="Dr. Seuss",
            a_status=published,
        )
        book.save()

    def test_login_page_ok(self):
        response = self.client.get('/accounts/login/')
        self.assertEqual(response.status_code, 200)

    def test_add_book_requires_login(self):
        #TODO this should end with a `/`
        url = '/book/add'
        response = self.client.get(url)
        self.assertRedirects(response, '/accounts/login/?next=%s' % url, status_code=302)

        response = self.client.post(url, {"title": "Computer Vision"})
        #TODO this should probably a 403
        self.assertRedirects(response, '/accounts/login/?next=%s' % url, status_code=302)

    def test_edit_book_requires_login(self):
        #TODO this should end with a `/`
        url = '/book/1/edit'
        response = self.client.get(url)
        self.assertRedirects(response, '/accounts/login/?next=%s' % url, status_code=302)

        response = self.client.put(url, {"title": "Two Scoops of Django"})
        #TODO this should probably a 403
        self.assertRedirects(response, '/accounts/login/?next=%s' % url, status_code=302)

    def test_remove_book_requires_login(self):
        #TODO this should end with a `/`
        url = '/book/1/remove'
        response = self.client.get(url)
        self.assertRedirects(response, '/accounts/login/?next=%s' % url, status_code=302)

        response = self.client.delete(url, {"title": "Two Scoops of Django"})
        #TODO this should probably a 403
        self.assertRedirects(response, '/accounts/login/?next=%s' % url, status_code=302)

    def test_add_language_requires_login(self):
        url = '/add/language/'
        response = self.client.get(url)
        self.assertRedirects(response, '/accounts/login/?next=%s' % url, status_code=302)

        response = self.client.post(url, {"title": "Two Scoops of Django"})
        #TODO this should probably a 403
        self.assertRedirects(response, '/accounts/login/?next=%s' % url, status_code=302)
