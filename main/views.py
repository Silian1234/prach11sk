import datetime
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *
from .utils import *
from django.views.generic import ListView
import json


def dig_pay(request):
    return render(request, 'main/digPay.html', {})


def fk_verify(request):
    return render(request, 'main/fk-verify.html', {})


class BlogListView(ListView):
    model = Post
    template_name = 'main/news.html'


def main_page(request):
    return render(request, 'main/mainPage.html', {})


def login_page(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.login()
            if user:
                login(request, user)
                return redirect('/profile')
    else:
        form = LoginForm()
    return render(request, 'main/login.html', {'form': form})


@login_required
def record(request):
    if Washes.objects.all().count() == 0 or datetime.now(
            tz=timezone.get_current_timezone()) > Washes.objects.last().date_time and datetime.now().strftime(
        '%a') != 'Sun':
        Washes.objects.all().delete()
        for d in generate_dates():
            wash = Washes.objects.create(date_time=d)
            wash.save()
    if request.method == 'POST':
        form = BookWashForm(request.POST)
        if form.is_valid():
            # print(form.cleaned_data)
            date_time = datetime.combine(form.cleaned_data['date'], form.cleaned_data['time'],
                                         timezone.get_current_timezone())
            washes = form.cleaned_data['washes']
            powder = form.cleaned_data['powder'] == 1
            selected_wash = Washes.objects.get(date_time=date_time)
            profile = Profile.objects.get(user_id=request.user.id)
            if powder and profile.wash_with >= washes:
                selected_wash.washes -= washes
                profile.wash_with -= washes
                profile.save()
            elif not powder and profile.wash_without >= washes:
                selected_wash.washes -= washes
                profile.wash_without -= washes
                profile.save()
            else:
                print('Недостаточно стирок на аккаунте')
            selected_wash.save()
            return HttpResponseRedirect('record')
    washes = Washes.objects.filter(date_time__gte=datetime.now(tz=timezone.get_current_timezone())).exclude(washes=0)
    date_and_time = {}
    for wash in washes:
        current_date = wash.date_time.strftime('%d.%m.%Y')
        time = wash.date_time.astimezone(timezone.get_current_timezone()).strftime('%H:%M')
        if current_date not in date_and_time.keys():
            date_and_time[current_date] = [(time, wash.washes)]
        else:
            date_and_time[current_date].append((time, wash.washes))
    date_dict = json.dumps(date_and_time)
    form = BookWashForm()
    return render(request, 'main/record.html', {'date_and_time': date_and_time, 'date_dict': date_dict, 'form': form})


@login_required
def payment(request):
    user = request.user
    if request.method == 'POST':
        form = CheckCodeForm(request.POST)
        if form.is_valid():
            unique_code = form.cleaned_data['unique_code']
            json = check_code(unique_code)
            if json['retval'] == 0:
                invoice = json['inv']
                if InvoiceNumber.objects.filter(invoice_number=invoice):
                    form.add_error(None, 'Такой код уже был использован!')
                else:
                    InvoiceNumber.objects.create(invoice_number=invoice)
                    profile = Profile.objects.get(user_id=user.id)
                    if json['id_goods'] == 3599100:
                        profile.wash_without += 1
                    elif json['id_goods'] == 3599134:
                        profile.wash_with += 1
                    profile.save()
                    return HttpResponseRedirect('profile')
            else:
                form.add_error(None, 'Несуществующий код!')
                print(form.errors)

    else:
        form = CheckCodeForm()
    return render(request, 'main/payment.html', {'form': form})


def news(request):
    return render(request, 'main/news.html', {})


def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/profile')
    else:
        form = RegistrationForm()
    return render(request, 'main/rega.html', {'form': form})


@login_required
def profile(request):
    return render(request, 'main/profile.html')
