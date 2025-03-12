from django.test import TestCase


class ViewTests(TestCase):
    def test_login(self):
        data = {'username': ' ####### ', 'password': ' ####### '}
        response = self.client.post('/login/', data=data)
        self.assertEqual(response.status_code, 200)

    # def test_homepage(self):
    #     response = self.client.get('/homepage/')
    #     self.assertTrue(b'Welcome to the Homepage' in response.content)

    def test_welcome(self):
        response = self.client.get('/hello/')
        data = response.json()
        self.assertEqual(data.get('msg'), 'Hello GET!')

    # def test_string_welcome(self):
    #     response = self.client.get('/hello/')
    #     string_data = response.content.decode('utf-8')
    #     self.assertEqual('Hello GET!', string_data)
