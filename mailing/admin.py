from django.contrib import admin
from mailing.models import Client, MailingModel, Message, MailingList, LogList


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'mail', 'is_active')
    list_filter = ('mail', )


@admin.register(MailingModel)
class MailingModelAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'time_from', 'time_to', 'week_day', 'description', 'sent')
    list_filter = ('name', )


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'title', 'message')


@admin.register(MailingList)
class MailingListAdmin(admin.ModelAdmin):
    list_display = ('pk', 'mailing', 'client')


@admin.register(LogList)
class LogListAdmin(admin.ModelAdmin):
    list_display = ('pk', 'time', 'error_type', 'error_message')