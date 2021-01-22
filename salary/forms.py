from django import forms
from .models import Salary


class SalaryForm(forms.ModelForm):

    class Meta:
        model = Salary
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(SalaryForm, self).__init__(*args, **kwargs)
