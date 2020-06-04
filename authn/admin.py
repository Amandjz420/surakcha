from django.contrib import admin

from .models import LoginOtpLog, User


@admin.register(LoginOtpLog)
class LoginOtpLogAdmin(admin.ModelAdmin):
    list_display = [f.name for f in LoginOtpLog._meta.fields]

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = [f.name for f in User._meta.fields]

