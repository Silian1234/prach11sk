from django.forms import ModelForm, TextInput, CharField, Form, PasswordInput
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class LoginForm(ModelForm):
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
        }

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

