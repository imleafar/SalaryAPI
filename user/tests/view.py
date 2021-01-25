from django.test import TestCase
from django.contrib import auth
from rest_framework.test import APIClient
from rest_framework.reverse import reverse
from django.contrib.auth.models import User as Account

from user.models import User
import user.templates
from user.views import user_list

from datetime import date


class TestUserViews(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.account = Account.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        self.credentials = {
            'username': 'john',
            'password': 'johnpassword'
        }

    def test_login_already_authenticated(self):
        self.client.login(username='john', password='johnpassword')
        response = self.client.get('/login/', follow=True)
        self.assertRedirects(response, '/users/', status_code=302, target_status_code=200, fetch_redirect_response=True)

    def test_login_success(self):
        response = self.client.post('/login/', self.credentials, follow=True)
        account = auth.get_user(self.client)
        self.assertTrue(account.is_authenticated)
        self.assertTrue(response.context['user'].is_active)
        self.assertRedirects(response, '/users/', status_code=302, target_status_code=200, fetch_redirect_response=True)

    def test_login_fail(self):
        response = self.client.post('/login/', {'username': 'josh', 'password': 'password'}, follow=True)
        message = str(response.content).split('id="messages">')[1].split('<')[0]
        self.assertEqual(message, 'Username or password is incorrect')

    def test_logout(self):
        self.client.login(username='john', password='johnpassword')
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)

    def test_user_list(self):
        self.client.login(username='john', password='johnpassword')
        response = self.client.get(reverse('user_list'))
        self.assertEqual(response.status_code, 200)

    def test_users_func(self):
        self.client.login(username='john', password='johnpassword')
        response = self.client.get(reverse('user_list'))
        self.assertEqual(response.resolver_match.func, user_list)
        self.assertEqual(response.resolver_match.func.__name__, user_list.__name__)

    def test_register_view_get(self):
        response = self.client.get('/register/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/register.html')
        self.failUnless(isinstance(response.context['form'], user.forms.CreateAccountForm))

    def test_register_view_post_success(self):
        response = self.client.post(reverse('register'), data={
            'username': 'alice',
            'email': 'alice@example.com',
            'password1': 'password000',
            'password2': 'password000'
            })
        self.assertRedirects(response, '/', status_code=302, target_status_code=200, fetch_redirect_response=True)
        self.assertEqual(Account.objects.count(), 2)

    def test_user_form_view_get(self):
        self.client.post('/login/', self.credentials, follow=True)
        response = self.client.get(reverse('user_insert'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_register/user_form.html')
        self.failUnless(isinstance(response.context['form'], user.forms.UserForm))

    def test_user_form_view_post_success(self):
        self.client.post('/login/', self.credentials, follow=True)
        data = {
            'cpf': '08191768933',
            'name': 'alice',
            'birth_day': date.today()
        }
        response = self.client.post(reverse('user_insert'), data, follow=True)
        response_update = self.client.get('/1/')
        response_updated = self.client.post('/1/', {
            'cpf': '08191768933',
            'name': 'lucas',
            'birth_day': date.today()
        }, follow=True)
        self.assertEqual(response_update.status_code, 200)
        self.assertRedirects(response, '/users/', status_code=302, target_status_code=200, fetch_redirect_response=True)
        self.assertRedirects(
            response_updated,
            '/users/',
            status_code=302,
            target_status_code=200
        )
        self.assertEqual(User.objects.count(), 1)

    def test_user_form_view_post_fail(self):
        self.client.post('/login/', self.credentials, follow=True)
        response = self.client.post(reverse('user_insert'), data={
            'cpf': '03834568923463',
            'name': 'robert',
            'birth_day': date.today()
        }, follow=True)
        self.assertEqual(response.content, b"<script>alert('Please do not try to insert fake data. "
                                           b"Date must be in mm/dd/yyyy format.')</script>")

    def test_user_delete_view(self):
        self.client.post('/login/', self.credentials, follow=True)
        self.client.post(reverse('user_insert'), data={
            'cpf': '08191768933',
            'name': 'anie',
            'birth_day': date.today()
        })
        response = self.client.get('/delete/1', follow=True)
        self.assertRedirects(response, '/users/', status_code=301, target_status_code=200, fetch_redirect_response=True)
