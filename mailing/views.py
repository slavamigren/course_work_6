from random import sample

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import render, redirect
from django.contrib.messages import success
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView

from blog.models import Blog
from mailing.forms import MailingModelForm, ClientForm, MessageForm
from mailing.models import Client, MailingModel, Message, MailingList, LogList
from django.conf import settings


class UserRequiredMixin:  # миксин блокирует доступ пользователя к чужим объектам
    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user:
            raise Http404
        return self.object


class MailinListView(LoginRequiredMixin, ListView):
    """Показывает страницу с рассылками пользователя"""
    model = MailingModel
    paginate_by = 10

    def get_queryset(self):
        return super().get_queryset().filter(
            owner=self.request.user
        )


class MailingDetailView(LoginRequiredMixin, UserRequiredMixin, DetailView):
    """Показыввает страницу с конкретной рассылкой, её деталями и списком включенных клиентов"""
    model = MailingModel


class MailingDeleteView(LoginRequiredMixin, UserRequiredMixin, DeleteView):
    """Удаляет рассылку пользователя"""
    model = MailingModel
    success_url = reverse_lazy('mailing:mailing_list')


class MailingCreateView(LoginRequiredMixin, CreateView):
    """Создаёт рассылку пользователя"""
    model = MailingModel
    form_class = MailingModelForm
    success_url = reverse_lazy('mailing:mailing_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)


class MailingUpdateView(LoginRequiredMixin, UserRequiredMixin, UpdateView):
    """Редактирует рассылку пользователя"""
    model = MailingModel
    form_class = MailingModelForm
    success_url = reverse_lazy('mailing:mailing_list')


@login_required
def change_mailing_is_active(request, **kwargs):
    """Отключает и включает рассылку, изменяя is_active в MailingModel"""
    model = MailingModel.objects.get(id=kwargs['pk'])
    if model.owner != request.user:
        raise Http404
    model.is_active = kwargs['act']
    model.save()
    return redirect(reverse('mailing:mailing_list'))


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

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)


class MessageDeleteView(LoginRequiredMixin, UserRequiredMixin, DeleteView):
    """Удаляет текст рассылки"""
    model = Message
    success_url = reverse_lazy('mailing:messages_list')


class MessageUpdateView(LoginRequiredMixin, UserRequiredMixin, UpdateView):
    """Редактирует текст рассылки"""
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mailing:messages_list')


class MessageDetailView(LoginRequiredMixin, UserRequiredMixin, DetailView):
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

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)


class ClientDeleteView(LoginRequiredMixin, UserRequiredMixin, DeleteView):
    """Удаляет клиента из базы для рассылок"""
    model = Client
    success_url = reverse_lazy('mailing:clients_list')


class ClientUpdateView(LoginRequiredMixin, UserRequiredMixin, UpdateView):
    """Редактирует клиента в базе для рассылок"""
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailing:clients_list')


class ClientDetailView(LoginRequiredMixin, UserRequiredMixin, DetailView):
    """Просмотр одного клиента из базы для рассылок"""
    model = Client


###########################################################################################################
# Блок добавления и удаления клиентов из рассылки
class RedactMailingClientsListView(LoginRequiredMixin, ListView):
    """Управляет страницей с добавлением и удалением клиентов из рассылки"""
    model = MailingList
    template_name = 'mailing/redact_mailing_clients.html'

    def get_context_data(self, **kwargs):
        # проверка, что данные запрашивает владелец
        if MailingModel.objects.get(id=self.kwargs['pk']).owner != self.request.user:
            raise Http404

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
    if Client.objects.get(id=kwargs['pk_client']).owner != request.user:  # проверка, что это клиент пользователя
        raise Http404
    MailingList.objects.create(mailing_model_id=kwargs['pk_mailindmodel'], client_id=kwargs['pk_client'], owner=request.user)
    return redirect(reverse('mailing:redact_mailing_clients', args=[kwargs['pk_mailindmodel']]))

@login_required
def delete_client_from_mailinglist(request, **kwargs):
    """Удаляет клиента из Client из рассылки MailingList"""
    instance = MailingList.objects.filter(mailing_model_id=kwargs['pk_mailindmodel'], client_id=kwargs['pk_client'])
    if instance[0].owner != request.user:  # проверка, что это клиент пользователя
        raise Http404
    instance.delete()
    return redirect(reverse('mailing:redact_mailing_clients', args=[kwargs['pk_mailindmodel']]))

@login_required
def delete_all_clients_from_mailinglist(request, **kwargs):
    """Добавляет всех не добавленных клиентов (хранятся Client) в рассылку MailingList"""
    instance = MailingList.objects.filter(mailing_model_id=kwargs['pk_mailindmodel'])
    if instance and instance[0].owner != request.user:  # проверка, что это клиент пользователя
        raise Http404
    instance.delete()
    return redirect(reverse('mailing:redact_mailing_clients', args=[kwargs['pk_mailindmodel']]))

@login_required
def add_all_clients_to_mailinglist(request, **kwargs):
    """Удаляет всех клиентов (хранятся Client) из рассылки MailingList"""
    if MailingModel.objects.get(id=kwargs['pk_mailindmodel']).owner != request.user:  # проверка, что это клиент пользователя
        raise Http404
    already_in_mailinglist = MailingList.objects.filter(mailing_model_id=kwargs['pk_mailindmodel'])
    emails_not_in_mailinglist = Client.objects.filter(owner=request.user)
    emails_not_in_mailinglist = emails_not_in_mailinglist.exclude(id__in=already_in_mailinglist.values_list('client_id', flat=True))
    mailing_list = []
    for client_id in emails_not_in_mailinglist.values_list('id', flat=True):
        mailing_list.append(
            MailingList(mailing_model_id=kwargs['pk_mailindmodel'], client_id=client_id, owner=request.user)
        )
    MailingList.objects.bulk_create(mailing_list)

    return redirect(reverse('mailing:redact_mailing_clients', args=[kwargs['pk_mailindmodel']]))
#####################################################################################################


@login_required
def main_page(request):
    """Главная страница"""

    #  выбираем три случайных поста из блога
    pks = list(Blog.objects.values_list('pk', flat=True))
    random_pk = sample(pks, 3)
    random_obj = Blog.objects.filter(pk__in=random_pk)

    #  выбираем общее количество рассылок и клиентов
    mailing_amount = (MailingModel.objects.filter(owner=request.user)).count()
    active_mailing_amount = (MailingModel.objects.filter(is_active=True, owner=request.user)).count()
    client_amount = (Client.objects.filter(owner=request.user)).count()

    context = {
        'object_list': random_obj,
        'mailing_amount': mailing_amount,
        'active_mailing_amount': active_mailing_amount,
        'client_amount': client_amount
    }

    return render(request, 'mailing/index.html', context)