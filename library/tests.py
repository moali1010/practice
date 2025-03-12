import datetime
from django.test import TestCase

from library.models import Author


# Create your tests here.
# type>> python manage.py test
class AuthorTests(TestCase):
    def setUp(self):
        Author.objects.create(first_name='Ali', last_name='Ebrahimi',
                              birth_date=datetime.date(2000, 4, 12), country="Iran")
        Author.objects.create(first_name='Maryam', last_name='Noori',
                              birth_date=datetime.date(1956, 11, 10), country="England")

    def test_is_young(self):
        ali = Author.objects.get(first_name='Ali')
        maryam = Author.objects.get(first_name='Maryam')
        self.assertTrue(ali.is_young())
        self.assertFalse(maryam.is_young())

    def test_is_old(self):
        ali = Author.objects.get(first_name='Ali')
        maryam = Author.objects.get(first_name='Maryam')
        self.assertFalse(ali.is_old())
        self.assertTrue(maryam.is_old())

    def test_str(self):
        ali = Author.objects.get(first_name='Ali', last_name='Ebrahimi')
        maryam = Author.objects.get(first_name='Maryam', last_name='Noori')
        self.assertEqual(ali.__str__(), 'Ali Ebrahimi')
        self.assertEqual(maryam.__str__(), 'Maryam Noori')
