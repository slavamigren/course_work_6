from django.shortcuts import render
from django.contrib.messages import success
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from mailing.models import Client, MailingModel, Message, MailingList, LogList
from django.core.mail import send_mail
from django.conf import settings


class MailingModelListView(ListView):
    model = MailingModel
    paginate_by = 10


class MailingDetailView(DetailView):
    model = MailingModel


class MailingDeleteView(DeleteView):
    model = MailingModel
    success_url = reverse_lazy('mailing:mailing_list')


class MailingCreateView(CreateView):
    model = MailingModel
    fields = ('name', 'time_from', 'time_to', 'week_day', 'description', 'message')
    success_url = reverse_lazy('mailing:mailing_list')


class MailingUpdateView(UpdateView):
    model = MailingModel
    fields = ('name', 'time_from', 'time_to', 'week_day', 'description', 'message')
    success_url = reverse_lazy('mailing:mailing_list')


class MessageListView(ListView):
    model = Message
    paginate_by = 10


class MessageCreateView(CreateView):
    model = Message
    fields = ('name', 'title', 'message')
    success_url = reverse_lazy('mailing:messages_list')


class MessageDeleteView(DeleteView):
    model = Message
    success_url = reverse_lazy('mailing:messages_list')


class MessageUpdateView(UpdateView):
    model = Message
    fields = ('name', 'title', 'message')
    success_url = reverse_lazy('mailing:messages_list')


class MessageDetailView(DetailView):
    model = Message


class LogListListView(ListView):
    model = LogList
    paginate_by = 10


class ClientListView(ListView):
    model = Client
    paginate_by = 10


class ClientCreateView(CreateView):
    model = Client
    fields = ('name', 'mail')
    success_url = reverse_lazy('mailing:clients_list')


class ClientDeleteView(DeleteView):
    model = Client
    success_url = reverse_lazy('mailing:clients_list')


class ClientUpdateView(UpdateView):
    model = Client
    fields = ('name', 'mail')
    success_url = reverse_lazy('mailing:clients_list')


class ClientDetailView(DetailView):
    model = Client


class MailingListDeleteView(DeleteView):
    model = MailingList


    def get_success_url(self):
        self.object = super().get_object()
        return reverse('mailing:detail_mailing', args=[self.object.mailing.pk])


class MailingListCreateView(CreateView):
    model = MailingList
    fields = ('mailing', 'client')


    def get_success_url(self):
        return reverse('mailing:detail_mailing', args=[self.kwargs['pk']])
