from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView
from django.conf import settings
from django.conf.urls.static import static
from  django.views.generic.base  import  TemplateView
from .views import *

urlpatterns = [
    path('', views.mainPage, name='mainPage'),
    path('profile', views.profile, name='profile'),
    #path('login', views.user_login, name='login'),
    path('rega', views.rega, name='rega'),
    path('profile', views.profile, name='profile'),
    path('record', views.record, name='record'),
    path('login', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='logout.html'), name='logout'),
    #path('news', views.news, name='news'),
    path('news', BlogListView.as_view(), name='news'),
    path('payment', views.payment, name='payment'),
    path('fk-verify', views.fkVerify, name='fk-verify')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)