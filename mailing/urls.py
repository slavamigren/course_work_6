from django.urls import path
from mailing.views import MailinListView, MessageListView, MessageCreateView, MessageDeleteView, \
    MessageUpdateView, MessageDetailView, MailingCreateView, MailingDeleteView, MailingUpdateView, MailingDetailView, \
    LogListListView, ClientListView, ClientCreateView, ClientDeleteView, ClientUpdateView, ClientDetailView, \
    RedactMailingClientsListView, add_client_to_mailinglist, \
    delete_client_from_mailinglist, delete_all_clients_from_mailinglist, add_all_clients_to_mailinglist
from mailing.apps import MailingConfig

app_name = MailingConfig.name


urlpatterns = [
    path('', MailinListView.as_view(), name='mailing_list'),

    path('create_mailing/', MailingCreateView.as_view(), name='create_mailing'),
    path('delete_mailing/<int:pk>/', MailingDeleteView.as_view(), name='delete_mailing'),
    path('update_mailing/<int:pk>/', MailingUpdateView.as_view(), name='update_mailing'),
    path('detail_mailing/<int:pk>/', MailingDetailView.as_view(), name='detail_mailing'),

    path('messages_list/', MessageListView.as_view(), name='messages_list'),
    path('create_message/', MessageCreateView.as_view(), name='create_message'),
    path('delete_message/<int:pk>/', MessageDeleteView.as_view(), name='delete_message'),
    path('update_message/<int:pk>/', MessageUpdateView.as_view(), name='update_message'),
    path('detail_message/<int:pk>/', MessageDetailView.as_view(), name='detail_message'),

    path('loglist_list/', LogListListView.as_view(), name='loglist_list'),

    path('clients_list/', ClientListView.as_view(), name='clients_list'),
    path('create_client/', ClientCreateView.as_view(), name='create_client'),
    path('delete_client/<int:pk>/', ClientDeleteView.as_view(), name='delete_client'),
    path('update_client/<int:pk>/', ClientUpdateView.as_view(), name='update_client'),
    path('detail_client/<int:pk>/', ClientDetailView.as_view(), name='detail_client'),
    
    path('redact_mailing_clients/<int:pk>/', RedactMailingClientsListView.as_view(), name='redact_mailing_clients'),
    path('add_client_to_mailinglist/<int:pk_client>/<int:pk_mailindmodel>/', add_client_to_mailinglist, name='add_client_to_mailinglist'),
    path('delete_client_to_mailinglist/<int:pk_client>/<int:pk_mailindmodel>/', delete_client_from_mailinglist, name='delete_client_to_mailinglist'),
    path('delete_all_clients_from_mailinglist/<int:pk_mailindmodel>/', delete_all_clients_from_mailinglist, name='delete_all_clients_from_mailinglist'),
    path('add_all_clients_to_mailinglist/<int:pk_mailindmodel>/', add_all_clients_to_mailinglist, name='add_all_clients_to_mailinglist'),

]