from django.contrib import admin
from main.models import *
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

admin.site.register(Post)
admin.site.register(InvoiceNumber)


class ProfileInLine(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Профиль'


class UserAdmin(BaseUserAdmin):
    inlines = [ProfileInLine]


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
