from django.urls import path
from mailing.views import MailingModelListView, MessageListView, MessageCreateView, MessageDeleteView, \
    MessageUpdateView, MessageDetailView, MailingCreateView, MailingDeleteView, MailingUpdateView, MailingDetailView, \
    LogListListView, ClientListView, ClientCreateView, ClientDeleteView, ClientUpdateView, ClientDetailView, \
    MailingListDeleteView, MailingListCreateView
from mailing.apps import MailingConfig

app_name = MailingConfig.name


urlpatterns = [
    path('', MailingModelListView.as_view(), name='mailing_list'),

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

    path('delete_client_from_mailing/<int:pk>/', MailingListDeleteView.as_view(), name='delete_client_from_mailing'),
    path('add_client_for_mailing/<int:pk>/', MailingListCreateView.as_view(), name='add_client_for_mailing'),

]