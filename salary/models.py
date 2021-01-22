from django.db import models

from user.models import User


class Salary(models.Model):
    cpf = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)
    date = models.DateField(auto_now=False, auto_now_add=False, blank=False, null=False)
    salary = models.DecimalField(max_digits=100, decimal_places=2, blank=False, null=False)
    discounts = models.DecimalField(max_digits=100, decimal_places=2, blank=False, null=False)
