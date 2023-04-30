from django import forms
from django.contrib.auth.forms import AuthenticationForm, UsernameField, UserCreationForm
from .models import *
from django.contrib.auth import authenticate


class CheckCodeForm(forms.Form):
    unique_code = forms.CharField(min_length=16, max_length=16, strip=True, widget=forms.TextInput(
        attrs={'class': "form__input", 'placeholder': 'Введите купленный код'}))


class BookWashForm(forms.Form):
    date = forms.DateField()
    time = forms.TimeField()
    washes = forms.IntegerField(max_value=2)
    powder = forms.IntegerField()


class ApplicationForm(forms.Form):
    room = forms.IntegerField(widget=forms.NumberInput(attrs={'min': '100', 'max': '550', 'class': 'form__input', 'placeholder': 'Комната/этаж, крыло'}))
    description = forms.CharField(widget=forms.TextInput(attrs={'class': 'form__input', 'placeholder': 'Описание проблемы'}))
    # user_id = forms.IntegerField(widget=forms.NumberInput(attrs={'type': 'hidden'}))

    def clean_room(self):
        room = self.cleaned_data.get('room')
        if room % 100 > 50:
            raise forms.ValidationError('Неверно указан номер комнаты!')
        return room

    def clean_description(self):
        if len(self.cleaned_data.get('description').split()) < 2:
            raise forms.ValidationError('Описание проблемы должно содержать минимум 2 слова!')
        return self.cleaned_data.get('description')


class StudyRoomForm(forms.Form):
    date = forms.DateField()
    choices = ((i, i) for i in range(10, 22))
    time = forms.MultipleChoiceField(choices=choices)
    people = forms.IntegerField()


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
        self.fields['username'].label = 'Придумайте логин'
        self.fields['password1'].label = 'Придумайте пароль'
        self.fields['password2'].label = 'Повторите пароль'
        self.fields['first_name'].widget.attrs.update({
            'required': 'True',
            'name': 'username',
            'type': 'text',
            'class': 'input1',
            'placeholder': 'Имя',
            'minlength': '2',
            'maxlength': '50'
        })
        self.fields['last_name'].widget.attrs.update({
            'required': 'True',
            'name': 'last_name',
            'type': 'text',
            'class': 'input1',
            'placeholder': 'Фамилия',
            'minlength': '2',
            'maxlength': '50'
        })
        self.fields['username'].widget.attrs.update({
            'required': 'True',
            'type': 'text',
            'class': 'input1',
            'placeholder': 'Логин',
            'minlength': '3',
            'maxlength': '40'
        })
        # self.fields['email'].widget.attrs.update({
        #     'required': 'True',
        #     'type': 'email',
        #     'class': 'input1',
        #     'placeholder': 'Email',
        # })
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
        fields = ['username', 'first_name', 'last_name', 'password1', 'password2']


class CreatePostForm(forms.Form):
    text = forms.CharField(required=True, widget=forms.Textarea(attrs={'class': 'form__textarea', 'placeholder': 'Выберите текст', 'rows': '2'}))