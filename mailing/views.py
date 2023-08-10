from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import render, redirect
from django.contrib.messages import success
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView

from mailing.forms import MailingModelForm, ClientForm, MessageForm
from mailing.models import Client, MailingModel, Message, MailingList, LogList
from django.core.mail import send_mail
from django.conf import settings


class MailinListView(LoginRequiredMixin, ListView):
    """Показывает страницу с рассылками пользователя"""
    model = MailingModel
    paginate_by = 10

    def get_queryset(self):
        return super().get_queryset().filter(
            owner=self.request.user
        )


class MailingDetailView(LoginRequiredMixin, DetailView):
    """Показыввает страницу с конкретной рассылкой, её деталями и списком включенных клиентов"""
    model = MailingModel


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    """Удаляет рассылку пользователя"""
    model = MailingModel
    success_url = reverse_lazy('mailing:mailing_list')


class MailingCreateView(LoginRequiredMixin, CreateView):
    """Создаёт рассылку пользователя"""
    model = MailingModel
    form_class = MailingModelForm
    success_url = reverse_lazy('mailing:mailing_list')


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    """Редактирует рассылку пользователя"""
    model = MailingModel
    form_class = MailingModelForm
    success_url = reverse_lazy('mailing:mailing_list')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user and not self.request.user.is_staff:
            raise Http404
        return self.object


class MessageListView(LoginRequiredMixin, ListView):
    """Показывает страницу с текстами рассылок"""
    model = Message
    paginate_by = 10

    def get_queryset(self):
        return super().get_queryset().filter(
            owner=self.request.user
        )


class MessageCreateView(LoginRequiredMixin, CreateView):
    """Создаёт новый текст рассылки"""
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mailing:messages_list')


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    """Удаляет текст рассылки"""
    model = Message
    success_url = reverse_lazy('mailing:messages_list')


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    """Редактирует текст рассылки"""
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mailing:messages_list')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user and not self.request.user.is_staff:
            raise Http404
        return self.object


class MessageDetailView(LoginRequiredMixin, DetailView):
    """Показывает детали текста рассылки"""
    model = Message


class LogListListView(LoginRequiredMixin, ListView):
    """Показывает журнал проведённых рассылок"""
    model = LogList
    paginate_by = 10

    def get_queryset(self):
        return super().get_queryset().filter(
            owner=self.request.user
        )


class ClientListView(LoginRequiredMixin, ListView):
    """Показывает всех клиентов для рассылок в базе"""
    model = Client
    paginate_by = 10

    def get_queryset(self):
        return super().get_queryset().filter(
            owner=self.request.user
        )


class ClientCreateView(LoginRequiredMixin, CreateView):
    """Добавляет клиента в базу для рассылок"""
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailing:clients_list')


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    """Удаляет клиента из базы для рассылок"""
    model = Client
    success_url = reverse_lazy('mailing:clients_list')


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    """Редактирует клиента в базе для рассылок"""
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailing:clients_list')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user and not self.request.user.is_staff:
            raise Http404
        return self.object


class ClientDetailView(LoginRequiredMixin, DetailView):
    """Просмотр одного клиента из базы для рассылок"""
    model = Client


# class MailingListDeleteView(DeleteView):
#     model = MailingList

    #
    # def get_success_url(self):
    #     self.object = super().get_object()
    #     return reverse('mailing:detail_mailing', args=[self.object.mailing_model.pk])


###########################################################################################################
# Блок добавления и удаления клиентов из рассылки

class RedactMailingClientsListView(LoginRequiredMixin, ListView):
    """Управляет страницей с добавлением и удалением клиентов из рассылки"""
    model = MailingList
    template_name = 'mailing/redact_mailing_clients.html'

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user and not self.request.user.is_staff:
            raise Http404
        return self.object

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        mailings = super().get_queryset().filter(mailing_model_id=self.kwargs['pk'])

        emails_not_in_mailinglist = Client.objects.filter(owner=self.request.user)
        emails_not_in_mailinglist = emails_not_in_mailinglist.exclude(id__in=mailings.values_list('client_id', flat=True))
        emails_in_mailinglist = Client.objects.filter(id__in=mailings.values_list('client_id', flat=True), owner=self.request.user)

        context_data['emails_not_in_mailinglist'] = emails_not_in_mailinglist
        context_data['emails_in_mailinglist'] = emails_in_mailinglist
        context_data['pk_mailindmodel'] = self.kwargs['pk']
        return context_data

    def get_queryset(self):
        return super().get_queryset().filter(
            mailing_model_id=self.kwargs['pk'],
            owner=self.request.user)


@login_required
def add_client_to_mailinglist(request, **kwargs):
    """Добавляет клиента из Client в рассылку MailingList"""
    MailingList.objects.create(mailing_model_id=kwargs['pk_mailindmodel'], client_id=kwargs['pk_client'])
    return redirect(reverse('mailing:redact_mailing_clients', args=[kwargs['pk_mailindmodel']]))

@login_required
def delete_client_from_mailinglist(request, **kwargs):
    """Удаляет клиента из Client из рассылки MailingList"""
    instance = MailingList.objects.filter(mailing_model_id=kwargs['pk_mailindmodel'], client_id=kwargs['pk_client'])
    instance.delete()
    return redirect(reverse('mailing:redact_mailing_clients', args=[kwargs['pk_mailindmodel']]))

@login_required
def delete_all_clients_from_mailinglist(request, **kwargs):
    """Добавляет всех не добавленных клиентов (хранятся Client) в рассылку MailingList"""
    instance = MailingList.objects.filter(mailing_model_id=kwargs['pk_mailindmodel'])
    instance.delete()
    return redirect(reverse('mailing:redact_mailing_clients', args=[kwargs['pk_mailindmodel']]))

@login_required
def add_all_clients_to_mailinglist(request, **kwargs):
    """Удаляет всех клиентов (хранятся Client) из рассылки MailingList"""

    already_in_mailinglist = MailingList.objects.filter(mailing_model_id=kwargs['pk_mailindmodel'])
    emails_not_in_mailinglist = Client.objects.exclude(id__in=already_in_mailinglist.values_list('client_id', flat=True))
    mailing_list = []
    for client_id in emails_not_in_mailinglist.values_list('id', flat=True):
        mailing_list.append(
            MailingList(mailing_model_id=kwargs['pk_mailindmodel'], client_id=client_id)
        )
    MailingList.objects.bulk_create(mailing_list)

    return redirect(reverse('mailing:redact_mailing_clients', args=[kwargs['pk_mailindmodel']]))

#####################################################################################################