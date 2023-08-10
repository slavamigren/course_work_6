from django.core.cache import cache
from django.core.management import BaseCommand
from mailing.models import Client, MailingModel, Message, MailingList, LogList
from datetime import datetime
from django.core.mail import send_mail
from django.conf import settings
from smtplib import SMTPException
import time


def check_adn_run_mailings():
    """Просматривает все рассылки, проверяет время, если время рассылки, отправляет письма"""
    if settings.CACHE_ENABLED:  # кешируем, чтобы не мучать бд каждую минуту
        key = 'all_mailings'
        all_mailings = cache.get(key)
        if all_mailings is None:
            all_mailings = MailingModel.objects.all()
            cache.set(key, all_mailings)
    else:
        all_mailings = MailingModel.objects.all()

    all_mailings = all_mailings.filter(is_active=True)  # оаставляем только активные рассылки

#    all_mailings = MailingModel.objects.all()
    current_time = datetime.now().time()
    current_week_day = datetime.now().isoweekday()

    for mailing in all_mailings:  # для каждой рассылки проверяем время и день недели
        if mailing.time_from <= current_time <= mailing.time_to and \
                (current_week_day == mailing.week_day or mailing.week_day is None):

            if not mailing.sent:  # проверяем флаг, что рассылка в указанное время ещё не производилась

                title = mailing.message.title  # забираем заголовок письма
                message = mailing.message.message  # забираем текст рассылки
                # выгружаем адреса клиентов
                emails_list = [letter.client.mail for letter in MailingList.objects.filter(mailing_model=mailing.pk)]

                try:
                    send_mail(title, message, settings.EMAIL_HOST_USER, emails_list)
                except Exception as err:  # записываем в лог, если были ошибки
                    loglist = LogList(mailing_model_id=mailing.pk, error_type=type(err), error_message=err.__str__())
                    loglist.save()
                else:  # если рассылка прошла, выставляем флаг
                    loglist = LogList(mailing_model_id=mailing.pk, error_type='successful!', error_message='successful!')
                    loglist.save()
                    record = MailingModel.objects.get(pk=mailing.pk)
                    record.sent = True
                    record.save(update_fields=['sent'])

        else:
            # если сейчас не время рассылки, но она производилась в прошедший период
            # и флаг ещё True, то сбрасываем его в False
            if mailing.sent:
                record = MailingModel.objects.get(pk=mailing.pk)
                record.sent = False
                record.save(update_fields=['sent'])

    print('!!!!!!!!!!!!!!!!!!!')