import json

from django.test import TestCase
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User, Permission
from library.models import Book, Author, Profile
from library.serializers import BookSerializer, ProfileSerializer


class ViewTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        add_book_perm = Permission.objects.get(codename='add_book')
        change_book_perm = Permission.objects.get(codename='change_book')
        delete_book_perm = Permission.objects.get(codename='delete_book')
        view_book_perm = Permission.objects.get(codename='view_book')
        self.user.user_permissions.add(add_book_perm, change_book_perm, delete_book_perm, view_book_perm)
        self.user.save()

        self.author = Author.objects.create(first_name='John', last_name='Doe', country='USA')
        self.book = Book.objects.create(title='Test Book', author=self.author, pages_count=100,
                                        publish_date='2023-01-01')
        self.profile = Profile.objects.create(user=self.user, phone_number='1234567890', country='USA')

    def test_login(self):
        data = {'username': 'testuser', 'password': 'testpass123'}
        response = self.client.post('/login/', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Logged in successfully!', response.content.decode())

    def test_signup(self):
        data = {
            'username': 'newuser',
            'password1': 'newpass123',
            'password2': 'newpass123',
            'country': 'USA'
        }
        response = self.client.post('/library/signup/', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('User created successfully!', response.content.decode())

    def test_user_list(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get('/user_list/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('testuser', response.content.decode())

    def test_register_user(self):
        data = {'username': 'newuser', 'password1': 'newpass123', 'password2': 'newpass123'}
        response = self.client.post('/register/', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('User Created!', response.content.decode())

    def test_logout_user(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get('/logout/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('You are logged out!', response.content.decode())

    def test_book_detail_update_delete(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(f'/books/{self.book.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Test Book', response.content.decode())

    def test_hello_view(self):
        response = self.client.get('/hello/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Hello GET!', response.content.decode())

    def test_book_list_api_view(self):
        response = self.client.get('/books/seri/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Test Book', response.content.decode())

    def test_book_list_create_api_view(self):
        self.client.login(username='testuser', password='testpass123')
        data = {
            'title': 'New Book',
            'author': self.author.id,
            'pages_count': 200,
            'publish_date': '2023-01-01'
        }
        response = self.client.post('/book-list-create/', data=data)
        self.assertEqual(response.status_code, 201)
        self.assertIn('New Book', response.content.decode())

    def test_book_retrieve_update_destroy_api_view(self):
        response = self.client.get(f'/books2/{self.book.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Test Book', response.content.decode())

    def test_new_logout(self):
        token = Token.objects.create(user=self.user)

        response = self.client.post('/logout2/', HTTP_AUTHORIZATION=f'Token {token.key}')

        self.assertEqual(response.status_code, 200)
        self.assertIn('You are logged out', response.content.decode())

    def test_add_book(self):
        self.client.login(username='testuser', password='testpass123')
        data = {'title': 'New Book', 'author': self.author.id, 'pages_count': 200, 'publish_date': '2023-01-01'}
        response = self.client.post('/library/add-book/', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Book added successfully', response.content.decode())

    def test_change_book(self):
        self.client.login(username='testuser', password='testpass123')
        data = {'title': 'Updated Book', 'author': self.author.id, 'pages_count': 150, 'publish_date': '2023-01-01'}
        response = self.client.post(f'/library/change-book/{self.book.id}/', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Book information updated!', response.content.decode())

    def test_delete_book(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.delete(f'/library/delete-book/{self.book.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Book deleted successfully!', response.content.decode())

    def test_view_book(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(f'/library/view-book/{self.book.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Test Book', response.content.decode())

    def test_book_list_create_api_view3_with_jwt(self):
        from rest_framework_simplejwt.tokens import AccessToken
        token = AccessToken.for_user(self.user)

        data = {'title': 'JWT Book', 'author': self.author.id, 'pages_count': 300, 'publish_date': '2023-01-01'}
        response = self.client.post(
            '/api/books/',
            data=data,
            HTTP_AUTHORIZATION=f'Bearer {token}'
        )
        self.assertEqual(response.status_code, 201)
        self.assertIn('JWT Book', response.content.decode())

    def test_view_book_not_found(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get('/library/view-book/999/')
        self.assertEqual(response.status_code, 404)
        self.assertIn('Book not found', response.content.decode())

    def test_book_serializer_invalid_data(self):
        invalid_data = {'title': '', 'author': self.author.id, 'pages_count': -100}
        serializer = BookSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('title', serializer.errors)
        self.assertIn('pages_count', serializer.errors)

    def test_book_detail_update_delete_put(self):
        self.client.login(username='testuser', password='testpass123')
        data = {'pages': 150}
        response = self.client.put(f'/books/{self.book.id}/', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.book.refresh_from_db()
        self.assertEqual(self.book.pages_count, 150)

    def test_book_detail_update_delete_delete(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.delete(f'/books/{self.book.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Book.objects.filter(id=self.book.id).exists())

    def test_signup_invalid_data(self):
        invalid_data = {'username': 'user', 'password1': 'pass', 'password2': 'pass', 'country': ''}
        response = self.client.post('/library/signup/', data=invalid_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('This field is required', response.content.decode())

    def test_change_password_wrong_old_password(self):
        self.client.login(username='testuser', password='testpass123')
        data = {'old_password': 'wrongpass', 'new_password1': 'newpass123', 'new_password2': 'newpass123'}
        response = self.client.post('/library/change-password/', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Wrong old password', response.content.decode())

    # def test_login(self):
    #     data = {'username': ' ####### ', 'password': ' ####### '}
    #     response = self.client.post('/login/', data=data)
    #     self.assertEqual(response.status_code, 200)

    # def test_homepage(self):
    #     response = self.client.get('/homepage/')
    #     self.assertTrue(b'Welcome to the Homepage' in response.content)

    # def test_welcome(self):
    #     response = self.client.get('/hello/')
    #     data = response.json()
    #     self.assertEqual(data.get('msg'), 'Hello GET!')

    # def test_string_welcome(self):
    #     response = self.client.get('/hello/')
    #     string_data = response.content.decode('utf-8')
    #     self.assertEqual('Hello GET!', string_data)
