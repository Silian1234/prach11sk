import datetime
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import *
from .models import *
from .utils import *
from django.views.generic import ListView
import json
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings


def is_wash_admin(user):
    return user.groups.filter(name__in=['Админ прачки']).exists()


def is_applications_admin(user):
    return user.groups.filter(name__in=['Админ журнала заявок']).exists()


def is_study_room_admin(user):
    return user.groups.filter(name__in=['Админ учебной комнаты']).exists()


def payment_digiseller(request):
    return render(request, 'main/digiseller-payment.html', {'settings': settings.WASH_ADMIN})


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
                                                            washes=washes, powder=powder)
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
                                                            washes=washes, powder=powder)
                wash_history.save()
                user.save()
                selected_wash.save()
                return redirect('profile')
            else:
                print('Недостаточно стирок на аккаунте')
                return redirect('book-wash')

    washes = Washes.objects.filter(date_time__gte=datetime.now(tz=timezone.get_current_timezone())).exclude(washes=0)
    date_and_time = {}
    ssk_group = request.user.groups.filter(name='ССК')
    for wash in washes:
        current_date = wash.date_time.strftime('%d.%m.%Y')
        day = wash.date_time.strftime('%a')
        time = wash.date_time.astimezone(timezone.get_current_timezone()).strftime('%H:%M')
        if not ssk_group and (day == 'Wed' or day == 'Sun'):
            continue
        wash_limit = 2 if request.user.profile.wash_limit > 2 else request.user.profile.wash_limit
        if current_date not in date_and_time:
            date_and_time[current_date] = [(time, wash_limit)]
        else:
            date_and_time[current_date].append((time, wash_limit))
    date_dict = json.dumps(date_and_time)
    form = BookWashForm()
    return render(request, 'main/book-wash.html',
                  {'date_and_time': date_and_time, 'date_dict': date_dict, 'form': form,
                   'settings': settings.WASH_ADMIN})


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
    washes = WashesHistory.objects.filter(date_time__gte=datetime.now(
        tz=timezone.get_current_timezone()) + timedelta(hours=-2), user=request.user).order_by('date_time')
    applications = Applications.objects.filter(user=request.user).filter(Q(status=0) | Q(status=1)).order_by(
        'created_at')
    study_room = StudyRoom.objects.filter(
        Q(date=datetime.now().date()) & Q(end_time__gte=datetime.now().time()) | Q(date__gt=datetime.now().date()),
        user=request.user).order_by('date', 'start_time')
    return render(request, 'main/profile.html',
                  {'washes': washes, 'applications': applications, 'study_room': study_room})


@csrf_exempt
@login_required
@user_passes_test(is_wash_admin)
def washes_admin(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        settings_key = data.get('key')
        value = data.get('value')
        if settings_key is not None and value is not None:
            if settings_key in settings.WASH_ADMIN:
                settings.WASH_ADMIN[settings_key] = value

    all_washes, washes_history = {}, {}
    wash_settings = False
    view = request.GET.get('view', None)
    limit_not_returned = WashesHistory.objects.filter(limit_returned=False, date_time__lt=datetime.now(
        tz=timezone.get_current_timezone()) + timedelta(hours=+2))

    for limit_return in limit_not_returned:
        limit_return.limit_returned = True
        if limit_return.user.profile.wash_limit < 2:
            limit_return.user.profile.wash_limit += 1
            limit_return.user.save()
        limit_return.save()

    if view == 'history':
        washes_history = WashesHistory.objects.filter(date_time__lt=datetime.now(
            tz=timezone.get_current_timezone()) + timedelta(hours=-2)).order_by('-date_time')
    elif view == 'settings':
        wash_settings = True
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
    return render(request, 'main/washes-admin.html',
                  {'washes_history': all_washes, 'wash_settings': wash_settings, 'settings': settings.WASH_ADMIN})


@csrf_exempt
@login_required
@user_passes_test(is_applications_admin)
def applications_admin(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        application_id = data.get('id')
        value = data.get('value')
        if application_id is not None and value is not None:
            application = Applications.objects.get(pk=int(application_id))
            application.status = value
            application.save()
    return render(request, 'main/applications-admin.html', {'applications': Applications.objects.all()})


@login_required
def applications(request):
    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            room = form.cleaned_data['room']
            descr = form.cleaned_data['description']
            application = Applications(room=room, full_name=f'{request.user.first_name} {request.user.last_name}',
                                       description=descr, user=request.user,
                                       created_at=datetime.now(tz=timezone.get_current_timezone()), status=0)
            application.save()
            return redirect('profile')
    else:
        form = ApplicationForm()
    return render(request, 'main/applications.html', {'form': form})


@login_required
def study_room(request):
    if request.method == 'POST':
        form = StudyRoomForm(request.POST)
        if form.is_valid():
            study_date = form.cleaned_data['date']
            start_time = form.cleaned_data['time'][0]
            end_time = int(form.cleaned_data['time'][-1]) + 1
            people = form.cleaned_data['people']
            study_room = StudyRoom.objects.create(date=study_date, start_time=start_time, end_time=str(end_time),
                                                  people=people, user=request.user)
            study_room.save()
            return redirect('profile')
    study_dates = {}
    for day in range(7):
        current_date = timedelta(days=+day) + date.today()
        occupied_times = StudyRoom.objects.filter(date=current_date)
        restricted_hours = [j for occupied_time in occupied_times for j in
                            range(occupied_time.start_time.hour, occupied_time.end_time.hour)]
        hours = []
        start_time = 10 if current_date != date.today() else datetime.now().time().hour + 1
        for start_hour in range(start_time, 22):
            if start_hour not in restricted_hours:
                hours.append(start_hour)
        study_dates[current_date.strftime('%d.%m.%Y')] = hours
    study_time = json.dumps(study_dates)
    return render(request, 'main/study-room.html', {'study_time': study_time, 'study_dates': study_dates})


@login_required
def menu(request):
    return render(request, 'main/menu.html')


@login_required
def history(request):
    history = []
    washes_history = WashesHistory.objects.filter(user=request.user).filter(date_time__lt=datetime.now(
        tz=timezone.get_current_timezone()) + timedelta(hours=-2)).order_by('-date_time')
    applications_history = Applications.objects.filter(user=request.user).filter(status=2).order_by('-created_at')
    study_room_history = StudyRoom.objects.filter(user=request.user).filter(
        Q(date=datetime.now().date()) & Q(end_time__lt=datetime.now().time()) | Q(date__lt=datetime.now().date()))
    for wash_history in washes_history:
        wash_date1 = wash_history.date_time.date().strftime('%d %B %Y г.').lower()
        wash_date2 = wash_history.date_time.date().strftime('%d.%m.%Y')
        wash_time = wash_history.date_time.astimezone(timezone.get_current_timezone()).time().strftime("%H:%M")
        washing_machine = format_washing_machines(wash_history.washes)
        history.append({
            'date': f'{wash_date1} {wash_time}',
            'name': 'Прачечная', 'status': 'Завершена',
            'description': f'{wash_date2} на {wash_time} {wash_history.washes} {washing_machine} {"с порошком" if wash_history.powder else "без порошка"}'})

    for study_info in study_room_history:
        date1 = study_info.date.strftime('%d %B %Y г.').lower()
        date2 = study_info.date.strftime('%d.%m.%Y')
        start_time = study_info.start_time.strftime("%H:%M")
        end_time = study_info.end_time.strftime("%H:%M")
        history.append({
            'date': f'{date1} {start_time}',
            'name': 'Учебная комната', 'status': 'Завершена',
            'description': f'{date2} на {start_time} - {end_time} {study_info.people} {format_people(study_info.people)}'})

    for application in applications_history:
        date1 = application.created_at.astimezone(timezone.get_current_timezone()).strftime('%d %B %Y г.').lower()
        application_time = application.created_at.astimezone(timezone.get_current_timezone()).strftime("%H:%M")
        history.append({
            'date': f'{date1} {application_time}',
            'name': 'Журнал заявок', 'status': application.get_status_display().lower(),
            'description': f'{application.description.lower()}'})
    return render(request, 'main/history.html', {'history': sorted(history, key=lambda item: item['date'])})


@login_required
@user_passes_test(is_study_room_admin)
def study_room_admin(request):
    view = request.GET.get('view', None)
    study_info = {}
    if view:
        study_room = StudyRoom.objects.filter(user=request.user).filter(
            Q(date=datetime.now().date()) & Q(end_time__lt=datetime.now().time()) | Q(date__lt=datetime.now().date()))
    else:
        study_room = StudyRoom.objects.filter(
            Q(date=datetime.now().date()) & Q(end_time__gte=datetime.now().time()) | Q(date__gt=datetime.now().date()),
            user=request.user).order_by('date', 'start_time')
    for info in study_room:
        if info.date.strftime('%d.%m.%Y') in study_info:
            study_info[info.date.strftime('%d.%m.%Y')].append({'start_time': info.start_time, 'end_time': info.end_time,
                                                               'full_name': f'{info.user.first_name} {info.user.last_name}',
                                                               'people': info.people, 'vk_id': info.user.profile.vk_id})
        else:
            study_info[info.date.strftime('%d.%m.%Y')] = [{'start_time': info.start_time, 'end_time': info.end_time,
                                                           'full_name': f'{info.user.first_name} {info.user.last_name}',
                                                           'people': info.people, 'vk_id': info.user.profile.vk_id}]
    return render(request, 'main/study-room-admin.html', {'study_info': study_info})
