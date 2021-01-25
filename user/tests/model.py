from django.test import TestCase
from user.models import User

from datetime import date


class TestUserModels(TestCase):

    def setUp(self):
        User.objects.create(cpf="08784763233", name="test", birth_day=date.today())

    def test_if_user_is_created(self):
        self.assertEqual(User.objects.count(), 1)

    def test_model_str(self):
        user = User.objects.get(pk=1)
        self.assertEqual(str(user), "08784763233")
