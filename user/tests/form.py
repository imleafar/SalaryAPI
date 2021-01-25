from django.test import TestCase

from user.forms import UserForm
from user.models import User

from datetime import date


class UserFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(cpf="08191768933", name="user", birth_day=date.today())

    def test_user_form_valid(self):
        data = {
            'cpf': '08191768933',
            'name': 'robert',
            'birth_day': date.today()
        }
        form = UserForm(data=data)
        self.assertTrue(form.is_valid())

    def test_user_form_invalid(self):
        data = {
            'cpf': '03834568923463',
            'name': 'robert',
            'birth_day': date.today()
        }
        form = UserForm(data=data)
        self.assertFalse(form.is_valid())
