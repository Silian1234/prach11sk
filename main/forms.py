from django.core.exceptions import ValidationError
from django.forms import ModelForm, TextInput
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UsernameField
from .models import *


class CheckCodeForm(forms.Form):
    unique_code = forms.CharField(min_length=16, max_length=16, strip=True, widget=forms.TextInput(
        attrs={'class': "input2"}))


class BookWashForm(forms.Form):
    date = forms.DateField()
    time = forms.TimeField()
    washes = forms.IntegerField()
    powder = forms.IntegerField()


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = UsernameField(required=True, widget=forms.TextInput(
        attrs={'class': 'input1', 'placeholder': 'Логин'}))
    password = forms.CharField(required=True, widget=forms.PasswordInput(
        attrs={
            'class': 'input1',
            'placeholder': 'Пароль',
        }
    ))


class RegaForm(ModelForm):
    class Meta:
        model = User
        fields = [
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
