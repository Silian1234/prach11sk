from django.forms import ModelForm, TextInput, CharField, Form, PasswordInput
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django.core.exceptions import ValidationError
from .models import *

class AddWashForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(AddWashForm, self).__init__(*args, *kwargs)

    def clean_account(self):
        form_account = self.cleaned_data.get('key_with')
        existing1 = KeyWith.objects.filter(client=self.user, account=form_account).exists()
        existing2 = KeyWithout.objects.filter(client=self.user, account=form_account).exists()
        if not existing1:
            print(11)
            raise ValidationError('Такого кода не существует')

        return form_account

    class Meta:
        model = KeyWith
        fields = ['key_with']


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = UsernameField(widget=forms.TextInput(
        attrs={'class': 'input1', 'placeholder': 'Логин'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'input1',
            'placeholder': 'Пароль',
        }
))

"""class LoginForm(ModelForm):
    class Meta:
        model = User
        fields =[
           'username', 'password'
        ]
        widgets = {
            "username": TextInput(attrs={
                'class': 'input1',
                'placeholder': 'Логин'
            }),
            "password": TextInput(attrs={
                'type': 'password',
                'class': 'input1',
                'placeholder': '*********'
            }),
        }"""

class RegaForm(ModelForm):
    class Meta:
        model = User
        fields =[
            'first_name', 'last_name', 'username', 'password', 'email'
        ]
        widgets = {
            "first_name": TextInput(attrs={
                'class': 'input1',
                'placeholder': 'Имя'
            }),
            "last_name": TextInput(attrs={
                'class': 'input1',
                'placeholder': 'Фамилия'
            }),
            "username": TextInput(attrs={
                'class': 'input1',
                'placeholder': 'Логин'
            }),
            "password": TextInput(attrs={
                'type': 'password',
                'class': 'input1',
                'placeholder': '*********'
            }),
            "email": TextInput(attrs={
               'class': 'input1',
               'placeholder': 'email'
            }),
        }

