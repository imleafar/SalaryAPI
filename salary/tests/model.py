from django.test import TestCase

from salary.models import Salary
from user.models import User

from datetime import date


class TestSalaryModels(TestCase):

    def setUp(self):
        user = User.objects.create(cpf="08784763233", name="test", birth_day=date.today())
        Salary.objects.create(cpf=user, date=date.today(), salary=123, discounts=123)

    def test_if_salary_is_created(self):
        self.assertEqual(Salary.objects.count(), 1)

    def test_model_str(self):
        salary = Salary.objects.get(pk=1)
        self.assertEqual(str(salary), "Salary object (1)")
