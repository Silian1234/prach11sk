from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime
from django.utils import timezone


class Post(models.Model):
    text = models.TextField('Статья')
    date = models.DateTimeField('Дата публикации')

    def __str__(self):
        return self.title


class InvoiceNumber(models.Model):
    invoice_number = models.CharField('Номер оплаченного счета', max_length=16)

    def __str__(self):
        return self.invoice_number


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    vk_id = models.IntegerField(default=-1)
    wash_limit = models.IntegerField(default=2)
    wash_with = models.IntegerField('Стирки с порошком', default=0)
    wash_without = models.IntegerField('Стирки без порошка', default=0)

    def __str__(self):
        return f'{self.user} Profile'

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()


class Washes(models.Model):
    date_time = models.DateTimeField('Дата и время стирки')
    washes = models.IntegerField('Количество оставшихся стирок', default=4)

    def __str__(self):
        return self.date_time.__str__()


class WashesHistory(models.Model):
    date_time = models.DateTimeField('Дата и время стирки')
    user_name = models.CharField('Фамилия и имя', max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    washes = models.IntegerField()
    limit_returned = models.BooleanField(default=False)
    powder = models.BooleanField()


class Applications(models.Model):
    room = models.IntegerField('Комната')
    full_name = models.CharField('Фамилия и имя', max_length=100)
    created_at = models.DateTimeField('Дата создания')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField('Описание проблемы')
    status_choices = ((0, 'Заявка подана'), (1, 'Заявка сделана'), (2, 'Заявка выполнена'))
    status = models.IntegerField(choices=status_choices)


class StudyRoom(models.Model):
    date = models.DateField('Дата')
    start_time = models.TimeField('Дата начала')
    end_time = models.TimeField('Дата окончания')
    people = models.IntegerField('Количество человек')
    user = models.ForeignKey(User, on_delete=models.CASCADE)