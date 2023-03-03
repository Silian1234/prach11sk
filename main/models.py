from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Post(models.Model):
    title = models.CharField('Название', max_length=50)
    anons = models.CharField('Анонс', max_length=250)
    full_text = models.TextField('Статья')
    date = models.DateTimeField('Дата публикации')

    def __str__(self):
        return self.title


class InvoiceNumber(models.Model):
    invoice_number = models.CharField('Номер оплаченного счета', max_length=16)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    wash_with = models.IntegerField('Стирки с порошком', default=0)
    wash_without = models.IntegerField('Стирки без порошка', default=0)

    def __str__(self):
        return f'{self.user} Profile'
