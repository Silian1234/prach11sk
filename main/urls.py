from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView
from django.conf import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = [
    path('', views.main_page, name='mainPage'),
    path('profile', views.profile, name='profile'),
    path('rega', views.rega, name='rega'),
    path('profile', views.profile, name='profile'),
    path('record', views.record, name='record'),
    path('login', LoginView.as_view(template_name='main/login.html', authentication_form=UserLoginForm), name='login'),
    path('logout/', LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('news', BlogListView.as_view(), name='news'),
    path('digPay', views.dig_pay, name='digPay'),
    path('payment', views.payment, name='payment'),
    path('fk-verify.html', views.fk_verify, name='fk-verify')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)