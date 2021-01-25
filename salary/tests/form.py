from django.test import TestCase

from salary.forms import SalaryForm
from salary.models import Salary
from user.models import User

from datetime import date


class UserFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(cpf="08191768933", name="user", birth_day=date.today())

    def test_salary_form_valid(self):
        data = {
            'cpf': 1,
            'date': date.today(),
            'salary': 1234,
            'discounts': 123
        }
        form = SalaryForm(data=data)
        self.assertTrue(form.is_valid())

    def test_user_form_invalid(self):
        data = {
            'cpf': 1,
            'date': 'wrong date',
            'salary': 1234,
            'discounts': 123
        }
        form = SalaryForm(data=data)
        self.assertFalse(form.is_valid())
