from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.reverse import reverse
from django.contrib.auth.models import User as Account

from user.models import User
from salary.models import Salary

import salary.templates
from salary.views import salary_list

from datetime import date


class TestSalaryViews(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.account = Account.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        self.credentials = {
            'username': 'john',
            'password': 'johnpassword'
        }

    def test_salary_list(self):
        self.client.login(username='john', password='johnpassword')
        response = self.client.get(reverse('salary_list'))
        self.assertEqual(response.status_code, 200)

    def test_salary_func(self):
        self.client.login(username='john', password='johnpassword')
        response = self.client.get(reverse('salary_list'))
        self.assertEqual(response.resolver_match.func, salary_list)
        self.assertEqual(response.resolver_match.func.__name__, salary_list.__name__)

    def test_salary_delete_view(self):
        self.client.post('/login/', self.credentials, follow=True)
        user = User.objects.create(cpf="08191768933", name="test", birth_day=date.today())
        Salary.objects.create(cpf=user, date=date.today(), salary=123, discounts=123)
        response = self.client.get('/salary/delete/1/', follow=True)
        self.assertRedirects(
            response,
            '/salaries/',
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True)

    def test_salary_form_view_get(self):
        self.client.post('/login/', self.credentials, follow=True)
        response = self.client.get(reverse('salary_insert'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'salary_register/salary_form.html')
        self.failUnless(isinstance(response.context['form'], salary.forms.SalaryForm))

    def test_salary_form_view_post_success(self):
        self.client.post('/login/', self.credentials, follow=True)
        User.objects.create(cpf="08191768933", name="test", birth_day=date.today())
        data = {
            'cpf': 1,
            'date': date.today(),
            'salary': 123,
            'discounts': 123
        }
        response = self.client.post(reverse('salary_insert'), data=data, follow=True)
        response_update = self.client.get('/salary/1/')
        response_updated = self.client.post('/salary/1/', {
            'cpf': 1,
            'date': date.today(),
            'salary': 1234,
            'discounts': 123
        }, follow=True)
        self.assertEqual(response_update.status_code, 200)
        self.assertRedirects(
            response,
            '/salaries/',
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True
        )
        self.assertRedirects(
            response_updated,
            '/salaries/',
            status_code=302,
            target_status_code=200
        )
        self.assertEqual(Salary.objects.count(), 1)

    def test_salary_form_view_post_fail(self):
        self.client.post('/login/', self.credentials, follow=True)
        response = self.client.post(reverse('salary_insert'), data={
            'cpf': '1',
            'date': date.today(),
            'salary': 1234,
            'discounts': 123
        }, follow=True)
        self.assertEqual(response.content, b"<script>alert('Please do not try to insert fake data. "
                                           b"Date must be in mm/dd/yyyy format.')</script>")
