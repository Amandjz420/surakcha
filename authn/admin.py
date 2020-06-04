from django.contrib import admin

from .models import LoginOtpLog


@admin.register(LoginOtpLog)
class LoginOtpLogAdmin(admin.ModelAdmin):
    list_display = [f.name for f in LoginOtpLog._meta.fields]

