from django import forms
from .models import User
from django.contrib.auth.models import User as Account
from django.contrib.auth.forms import UserCreationForm


class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)


class CreateAccountForm(UserCreationForm):
    class Meta:
        model = Account
        fields = ['username', 'email', 'password1', 'password2']
