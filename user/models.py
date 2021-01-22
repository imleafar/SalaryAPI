from django.db import models

from cpf_field.models import CPFField


class User(models.Model):
    cpf = CPFField()
    name = models.CharField(max_length=250, blank=False, null=False)
    birth_day = models.DateField(auto_now=False, auto_now_add=False, blank=False, null=False)

    def __str__(self):
        return self.cpf
