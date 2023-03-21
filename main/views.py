import datetime
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import *
from .models import *
from .utils import *
from django.views.generic import ListView
import json


def is_admin(user):
    return user.groups.filter(name__in=['Админ прачки']).exists()


def payment_digiseller(request):
    return render(request, 'main/digiseller-payment.html', {})


def fk_verify(request):
    return render(request, 'main/fk-verify.html', {})


class BlogListView(ListView):
    model = Post
    template_name = 'main/news.html'


def main_page(request):
    return render(request, 'main/main.html', {})


def login_page(request):
    next = 'profile'
    if request.method == 'POST':
        form = LoginForm(request.POST)
        next = request.POST['next']
        if form.is_valid():
            user = form.login()
            if user:
                login(request, user)
                return redirect(next)
    else:
        if request.GET.get('next'):
            next = request.GET['next']
        form = LoginForm()
    return render(request, 'main/login.html', {'form': form, 'next': next})


@login_required
def book_wash(request):
    if Washes.objects.all().count() == 0 or datetime.now(
            tz=timezone.get_current_timezone()) > Washes.objects.last().date_time:
        Washes.objects.all().delete()
        for d in generate_wash_dates():
            wash = Washes.objects.create(date_time=d)
            wash.save()

    if request.method == 'POST':
        form = BookWashForm(request.POST)
        if form.is_valid():
            date_time = datetime.combine(form.cleaned_data['date'], form.cleaned_data['time'],
                                         tzinfo=timezone.get_current_timezone())
            washes = form.cleaned_data['washes']
            powder = form.cleaned_data['powder'] == 1
            selected_wash = Washes.objects.get(date_time=date_time)
            user = User.objects.get(pk=request.user.id)
            if powder and user.profile.wash_with >= washes:
                selected_wash.washes -= washes
                user.profile.wash_with -= washes
                user.profile.wash_limit -= washes
                wash_history = WashesHistory.objects.create(date_time=date_time,
                                                            user_name=f'{user.first_name} {user.last_name}',
                                                            user=user,
                                                            washes=washes)
                wash_history.save()
                user.save()
                selected_wash.save()
                return redirect('profile')
            elif not powder and user.profile.wash_without >= washes:
                selected_wash.washes -= washes
                user.profile.wash_without -= washes
                user.profile.wash_limit -= washes
                wash_history = WashesHistory.objects.create(date_time=date_time,
                                                            user_name=f'{user.first_name} {user.last_name}',
                                                            user=user,
                                                            washes=washes)
                wash_history.save()
                user.save()
                selected_wash.save()
                return redirect('profile')
            else:
                print('Недостаточно стирок на аккаунте')
                return redirect('book-wash')
            # selected_wash.save()

    washes = Washes.objects.filter(date_time__gte=datetime.now(tz=timezone.get_current_timezone())).exclude(washes=0)
    date_and_time = {}
    ssk_group = request.user.groups.filter(name='ССК')
    for wash in washes:
        current_date = wash.date_time.strftime('%d.%m.%Y')
        day = wash.date_time.strftime('%a')
        time = wash.date_time.astimezone(timezone.get_current_timezone()).strftime('%H:%M')
        if not ssk_group and (day == 'Wed' or day == 'Sun'):
            continue
        if current_date not in date_and_time.keys():
            date_and_time[current_date] = [(time, request.user.profile.wash_limit)]
        else:
            date_and_time[current_date].append((time, request.user.profile.wash_limit))
    date_dict = json.dumps(date_and_time)
    form = BookWashForm()
    return render(request, 'main/book-wash.html',
                  {'date_and_time': date_and_time, 'date_dict': date_dict, 'form': form})


@login_required
def payment(request):
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
                    user = User.objects.get(pk=request.user.id)
                    if json['id_goods'] == 3599100:
                        user.profile.wash_without += 1
                    elif json['id_goods'] == 3599134:
                        user.profile.wash_with += 1
                    user.save()
                    return redirect('payment')
            else:
                form.add_error(None, 'Несуществующий код!')
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
            return redirect(get_auth_url())
    else:
        form = RegistrationForm()
    return render(request, 'main/registration.html', {'form': form})


@login_required
def profile(request):
    if request.GET.get('code', '') != '':
        json = get_access_token(request.GET['code'])
        if 'error' not in json:
            user = User.objects.get(pk=request.user.id)
            user.profile.vk_id = json['user_id']
            user.save()
    return render(request, 'main/profile.html')


@login_required
@user_passes_test(is_admin)
def washes_history(request):
    print(datetime.now(
        tz=timezone.get_current_timezone()))
    all_washes, washes_history = {}, {}
    view = request.GET.get('view', None)
    limit_not_returned = WashesHistory.objects.filter(limit_returned=False, date_time__lt=datetime.now(
        tz=timezone.get_current_timezone()) + timedelta(hours=+2))

    for limit_return in limit_not_returned:
        print(limit_return.user)
        limit_return.limit_returned = True
        # user = User.objects.get(pk=limit_return.user_id)
        if limit_return.user.profile.wash_limit < 2:
            limit_return.user.profile.wash_limit += 1
            limit_return.user.save()
        limit_return.save()

    if view == 'history':
        washes_history = WashesHistory.objects.filter(date_time__lt=datetime.now(
            tz=timezone.get_current_timezone()) + timedelta(hours=-2))
    elif view == 'settings':
        print('load settings')
    else:
        washes_history = WashesHistory.objects.filter(date_time__gte=datetime.now(
            tz=timezone.get_current_timezone()) + timedelta(hours=-2))

    for wash in washes_history:
        date_time = wash.date_time.astimezone(timezone.get_current_timezone())
        date = date_time.strftime('%d.%m.%Y')
        time = date_time.strftime('%H:%M')
        if date not in all_washes.keys():
            all_washes[date] = {}
        if date in all_washes.keys() and time not in all_washes[date].keys():
            all_washes[date][time] = [wash.user_name for _ in range(wash.washes)]
        else:
            for _ in range(wash.washes):
                all_washes[date][time].append(wash.user_name)
    return render(request, 'main/washes-history.html', {'washes_history': all_washes})


@login_required
def applications(request):
    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            room = form.cleaned_data['room']
            descr = form.cleaned_data['description']
            application = Applications(room=room, user_name=f'{request.user.first_name} {request.user.last_name}',
                                       description=descr, user=request.user)
            application.save()
            return redirect('profile')
    else:
        form = ApplicationForm()
    return render(request, 'main/applications.html', {'form': form})


@login_required
def menu(request):
    return render(request, 'main/menu.html')
