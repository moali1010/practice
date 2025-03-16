import datetime
from django.test import TestCase
from django.contrib.auth.models import User
from library.models import Author, Book, Profile


# Create your tests here.
# type>> python manage.py test
class ModelTests(TestCase):
    def setUp(self):
        self.author_young = Author.objects.create(
            first_name="John",
            last_name="Doe",
            birth_date=datetime.date(1995, 5, 15),
            country="USA"
        )
        self.author_old = Author.objects.create(
            first_name="Jane",
            last_name="Doe",
            birth_date=datetime.date(1955, 5, 15),
            country="UK"
        )
        self.author = Author.objects.create(
            first_name="George",
            last_name="Orwell",
            birth_date=datetime.date(1903, 6, 25),
            country="UK"
        )
        self.book = Book.objects.create(
            title="1984",
            publish_date=datetime.date(1949, 6, 8),
            pages_count=328,
            author=self.author
        )
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123"
        )
        self.profile = Profile.objects.create(
            user=self.user,
            phone_number="1234567890",
            country="Canada"
        )

    def test_is_young(self):
        self.assertTrue(self.author_young.is_young())
        self.assertFalse(self.author_old.is_young())

    def test_is_old(self):
        self.assertFalse(self.author_young.is_old())
        self.assertTrue(self.author_old.is_old())

    def test_author_str(self):
        self.assertEqual(str(self.author_young), "John Doe")
        self.assertEqual(str(self.author_old), "Jane Doe")

    def test_book_str(self):
        self.assertEqual(str(self.book), "1984")

    def test_book_author_relation(self):
        self.assertEqual(self.book.author.first_name, "George")
        self.assertEqual(self.book.author.last_name, "Orwell")

    def test_profile_str(self):
        self.assertEqual(str(self.profile), "testuser")

    def test_profile_user_relation(self):
        self.assertEqual(self.profile.user.username, "testuser")
        self.assertEqual(self.profile.country, "Canada")

    def test_profile_phone_number(self):
        self.assertEqual(self.profile.phone_number, "1234567890")


# python manage.py dumpdata library.Author library.Book auth.User library.Profile --indent 2 > library/fixtures/initial_data.json
class AuthorTests(TestCase):
    fixtures = ['authors_books.json']

    # def test_author_count(self):
    #     self.assertEqual(Author.objects.count(), 3)
    def test_book_relation(self):
        book = Book.objects.get(pk=1)
        self.assertEqual(book.author.first_name, "George")


class BookTests(TestCase):
    fixtures = ['authors_books.json']

    def test_book_str(self):
        book = Book.objects.get(title="1984")
        self.assertEqual(str(book), "1984")

    def test_profile_relation(self):
        profile = Profile.objects.get(pk=1)
        self.assertEqual(profile.user.username, "testuser")
