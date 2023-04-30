from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView
from django.conf import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = [
    path('', views.main_page, name='main'),
    path('registration', views.registration, name='registration'),
    path('profile', views.profile, name='profile'),
    path('book-wash', views.book_wash, name='book-wash'),
    path('login', views.login_page, name='login'),
    path('logout', LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('news', views.news, name='news'),
    path('payment/digiseller', views.payment_digiseller, name='payment-digiseller'),
    path('payment', views.payment, name='payment'),
    path('fk-verify.html', views.fk_verify, name='fk-verify'),
    path('washes-admin', views.washes_admin, name='washes-admin'),
    path('applications', views.applications, name='applications'),
    path('menu', views.menu, name='menu'),
    path('applications-admin', views.applications_admin, name='applications-admin'),
    path('study-room', views.study_room, name='study-room'),
    path('history', views.history, name='history'),
    path('study-room-admin', views.study_room_admin, name='study-room-admin')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)