from django.db import models
from django.utils import timezone

from conf import settings

NULLABLE = {'blank': True, 'null': True}

class Client(models.Model): # хранит имя клиента рассылки и его почту
    name = models.CharField(max_length=50, verbose_name='имя клиента')
    mail = models.EmailField(max_length=50, verbose_name='email клиента')
    is_active = models.BooleanField(default=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE,
                              verbose_name='пользователь')

    def __str__(self):
        return f'{self.name}: {self.mail}'

    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = 'клиенты'
        ordering = ['name']


class Message(models.Model): # хранит шаблон письма
    name = models.CharField(max_length=30, verbose_name='название')
    title = models.CharField(max_length=200, **NULLABLE, verbose_name='тема письма')
    message = models.TextField(verbose_name='сообщение')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE,
                              verbose_name='пользователь')

    def __str__(self):
        return f'{self.name}: {self.title}'


    class Meta:
        verbose_name = 'сообщение'
        verbose_name_plural = 'сообщения'
        ordering = ['name']


class MailingModel(models.Model): # хранит рассылку
    WEEK_DAYS = [
        ('1', 'Monday'),
        ('2', 'Tuesday'),
        ('3', 'Wednesday'),
        ('4', 'Thursday'),
        ('5', 'Friday'),
        ('6', 'Saturday'),
        ('7', 'Sunday')
    ]
    name = models.CharField(max_length=20, verbose_name = 'название рассылки')
    time_from = models.TimeField(auto_now=False, auto_now_add=False, verbose_name='начало рассылки')
    time_to = models.TimeField(auto_now=False, auto_now_add=False, verbose_name='окончание рассылки')
    week_day = models.CharField(max_length=1, choices=WEEK_DAYS, **NULLABLE, verbose_name='день недели')
    description = models.TextField(**NULLABLE, verbose_name='описание рассылки')
    message = models.ForeignKey(Message, on_delete=models.SET_NULL, **NULLABLE, verbose_name='текст рассылки')
    sent = models.BooleanField(default=False, verbose_name='рассылка проведена')
    is_active = models.BooleanField(default=False, verbose_name='активна')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE,
                              verbose_name='пользователь')

    def __str__(self):
        return f'{self.name}: weekday - {self.week_day}, time {self.time_from} - {self.time_to}'

    class Meta:
        verbose_name = 'рассылка'
        verbose_name_plural = 'рассылки'
        ordering = ['time_from']


class MailingList(models.Model): # хранит список рассылка-клиент
    mailing_model = models.ForeignKey(MailingModel, on_delete=models.CASCADE, verbose_name='рассылка')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='клиент')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE,
                              verbose_name='пользователь')

    def __str__(self):
        return f'{self.mailing_model}: -> {self.client}'

    class Meta:
        verbose_name = 'письмо'
        verbose_name_plural = 'письма'
        unique_together = ('mailing_model', 'client')


class LogList(models.Model): # лог ошибок и успехов при отправке почты
    mailing_model = models.ForeignKey(MailingModel, on_delete=models.CASCADE, **NULLABLE, verbose_name='рассылка')
    time = models.DateTimeField(default=timezone.now, verbose_name='время рассылки')
    error_type = models.CharField(max_length=50, verbose_name='успех / тип ошибки')
    error_message = models.TextField(verbose_name='успех / сообщение об ошибке')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE,
                              verbose_name='пользователь')

    class Meta:
        verbose_name = 'лог рассылки'
        verbose_name_plural = 'логи рассылки'
        ordering = ['-time']
