from django import forms
from django.contrib.auth.forms import AuthenticationForm, UsernameField, UserCreationForm
from .models import *
from django.contrib.auth import authenticate


class CheckCodeForm(forms.Form):
    unique_code = forms.CharField(min_length=16, max_length=16, strip=True, widget=forms.TextInput(
        attrs={'class': "input2"}))


class BookWashForm(forms.Form):
    date = forms.DateField()
    time = forms.TimeField()
    washes = forms.IntegerField()
    powder = forms.IntegerField()


class LoginForm(forms.Form):
    username = forms.CharField(min_length=3, max_length=40, required=True, widget=forms.TextInput(
        attrs={'class': 'input1', 'placeholder': 'Логин'}))
    password = forms.CharField(required=True, widget=forms.PasswordInput(
        attrs={
            'class': 'input1',
            'placeholder': 'Пароль',
        }
    ))

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if user is None or not user.is_active:
            raise forms.ValidationError("Неправильный логин или пароль!")
        return self.cleaned_data

    def login(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        return user


class RegistrationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].label = 'Введите ваше имя'
        self.fields['last_name'].label = 'Введите вашу фамилию'
        self.fields['email'].label = 'Введите ваш email'
        self.fields['username'].label = 'Придумайте логин'
        self.fields['password1'].label = 'Придумайте пароль'
        self.fields['password2'].label = 'Повторите пароль'
        self.fields['first_name'].widget.attrs.update({
            'required': 'True',
            'name': 'username',
            'type': 'text',
            'class': 'input1',
            'placeholder': 'Имя',
            'minlength': '3',
            'maxlength': '40'
        })
        self.fields['last_name'].widget.attrs.update({
            'required': 'True',
            'name': 'last_name',
            'type': 'text',
            'class': 'input1',
            'placeholder': 'Фамилия',
            'minlength': '3',
            'maxlength': '40'
        })
        self.fields['username'].widget.attrs.update({
            'required': 'True',
            'type': 'text',
            'class': 'input1',
            'placeholder': 'Логин',
            'minlength': '3',
            'maxlength': '40'
        })
        self.fields['email'].widget.attrs.update({
            'required': 'True',
            'type': 'email',
            'class': 'input1',
            'placeholder': 'Email',
            # 'minlength': '3',
            # 'maxlength': '40'
        })
        self.fields['password1'].widget.attrs.update({
            'required': 'True',
            'type': 'text',
            'class': 'input1',
            'placeholder': '**********',
            # 'minlength': '3',
            # 'maxlength': '40'
        })
        self.fields['password2'].widget.attrs.update({
            'required': 'True',
            'type': 'text',
            'class': 'input1',
            'placeholder': '**********',
            # 'minlength': '3',
            # 'maxlength': '40'
        })

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
# class RegaForm(UserCreationForm):
#
#     username = forms.CharField(min_length=3, max_length=40,
#                                widget=forms.TextInput(attrs={'class': 'input1', 'placeholder': 'Логин'}),
#                                label='Придумайте логин')
#     email = forms.EmailField(
#         widget=forms.EmailInput(attrs={'class': 'input1', 'placeholder': 'Email'}), label='Введите вашу почту')
#     password1 = forms.CharField(
#         widget=forms.PasswordInput(attrs={'class': 'input1', 'placeholder': '**********'}), label='Придумайте пароль')
#     password2 = forms.CharField(
#         widget=forms.PasswordInput(attrs={'class': 'input1', 'placeholder': '**********'}), label='Подтвердите пароль')
#     first_name = forms.CharField(min_length=2, max_length=40,
#                                  widget=forms.TextInput(attrs={'class': 'input1', 'placeholder': 'Имя'}),
#                                  label='Введите ваше имя')
#     last_name = forms.CharField(min_length=2, max_length=40,
#                                 widget=forms.TextInput(attrs={'class': 'input1', 'placeholder': 'Фамилия'}),
#                                 label='Введите вашу фамилию')
# class Meta:
#     model = User
#
# fields = [
#     'first_name', 'last_name', 'username', 'email', 'password1', 'password2'
# ]
# # fields = '__all__'
# widgets = {
#     "first_name": forms.TextInput(attrs={
#         'class': 'input1',
#         'placeholder': 'Имя',
#     }),
#     "last_name": forms.TextInput(attrs={
#         'class': 'input1',
#         'placeholder': 'Фамилия'
#     }),
#     "username": forms.TextInput(attrs={
#         'class': 'input1',
#         'placeholder': 'Логин'
#     }),
#
#     "email": forms.TextInput(attrs={
#         'class': 'input1',
#         'placeholder': 'email'
#     }),
#     "password1": forms.TextInput(attrs={
#         'type': 'password',
#         'class': 'input1',
#         'placeholder': '*********'
#     }),
#     "password2": forms.PasswordInput(attrs={
#         'type': 'password',
#         'class': 'input1',
#         'placeholder': '*********'
#     }),
# }
