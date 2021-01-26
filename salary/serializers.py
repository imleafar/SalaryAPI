from rest_framework import serializers

from .models import Salary


class SalarySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Salary
        fields = ('cpf', 'date', 'salary', 'discounts')
