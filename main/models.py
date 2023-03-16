from django.db import models
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

    def __str__(self):
        return self.invoice_number


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    wash_with = models.IntegerField('Стирки с порошком', default=0)
    wash_without = models.IntegerField('Стирки без порошка', default=0)

    def __str__(self):
        return f'{self.user} Profile'


class Washes(models.Model):
    date_time = models.DateTimeField('Дата и время стирки')
    washes = models.IntegerField('Количество оставшихся стирок', default=2)

    def __str__(self):
        return self.date_time.__str__()


class WashesHistory(models.Model):
    date_time = models.DateTimeField('Дата и время стирки')
    user = models.CharField('Фамилия и имя', max_length=100)
    washes = models.IntegerField('Количество стирок', default=1)

    def __str__(self):
        return self.user


class Applications(models.Model):
    room = models.IntegerField('Комната')
    user = models.CharField('Фамилия и имя', max_length=100)
    description = models.TextField('Описание проблемы')

    def __str__(self):
        return self.room