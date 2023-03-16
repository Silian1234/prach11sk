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
    path('news', BlogListView.as_view(), name='news'),
    path('payment/digiseller', views.payment_digiseller, name='payment-digiseller'),
    path('payment', views.payment, name='payment'),
    path('fk-verify.html', views.fk_verify, name='fk-verify'),
    path('history', views.history, name='history'),
    path('applications', views.applications, name='applications'),
    path('menu', views.menu, name='menu')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)