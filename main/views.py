from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth import logout, login
from .forms import *
from .models import *
from .utils import *
from django.views.generic import ListView
from django.db.models import F
from django.contrib.auth.models import User


def digPay(request):
    return render(request, 'main/digPay.html', {})


# def payment(request):
#     return render(request, '')

"""def add(request):
    if request.method == "POST":
        keys = Keys()
        keys.key = keyGenerator(1)
        keys.save()"""


def fkVerify(request):
    return render(request, 'main/fk-verify.html', {})


class BlogListView(ListView):
    model = Post
    template_name = 'main/news.html'


"""def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenticated successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'main/login.html', {'form': form})"""


def mainPage(request):
    return render(request, 'main/mainPage.html', {})


def login(request):
    return render(request, 'main/login.html', {})


@login_required
def record(request):
    return render(request, 'main/record.html', {})


"""@login_required
def payment(request):
    #keysWithout = KeyWithout.objects.all()
    #keysWith = KeyWith.objects.all()
    return render(request, 'main/payment.html', {})"""


@login_required
def payment(request):
    user = request.user
    if request.method == 'POST':
        form = WashForm(request.POST)
        if form.is_valid():
            unique_code = form.cleaned_data['unique_code']
            json = check_code(unique_code)
            if json['retval'] == 0:
                invoice = json['inv']
                if InvoiceNumber.objects.filter(invoice_number=invoice):
                    print('code already exists')
                else:
                    InvoiceNumber.objects.create(invoice_number=invoice)
                    profile = Profile.objects.get(user_id=user.id)
                    if json['id_goods'] == 3599100:
                        profile.wash_without += 1
                    elif json['id_goods'] == 3599134:
                        profile.wash_with += 1
                    profile.save()
    form = WashForm()
    return render(request, 'main/payment.html', {'form': form})
    #     form = AddWashForm(request.POST, user=request.user)
    #     if form.is_valid():
    #         payment = form.save(commit=False)
    #         payment.save()
    #         print(2)
    # else:
    #     form = AddWashForm()


def news(request):
    return render(request, 'main/news.html', {})


def rega(request):
    if request.method == 'POST':
        form = RegaForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            """new_user.set_username(form.cleaned_data['username'])
            new_user.set_first_name(form.cleaned_data['first_name'])
            new_user.set_last_name(form.cleaned_data['last_name'])
            new_user.set_email(form.cleaned_data['email'])"""
            new_user.save()
            return render(request, 'main/successRega.html', {'new_user': new_user})
    else:
        form = RegaForm()
    return render(request, 'main/rega.html', {'form': form})


@login_required
def profile(request):
    return render(request, 'main/profile.html')
