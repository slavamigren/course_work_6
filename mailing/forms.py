from django import forms
from django.forms import BaseFormSet

from mailing.models import MailingModel, Client, Message


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class MailingModelForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = MailingModel
        fields = ('name', 'time_from', 'time_to', 'week_day', 'description', 'message', 'is_active')

    def __init__(self, *args, **kwargs):
       user = kwargs.pop('user')
       super().__init__(*args, **kwargs)
       self.fields['message'].queryset = Message.objects.filter(owner=user)


class ClientForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Client
        fields = ('name', 'mail')


class MessageForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Message
        fields = ('name', 'title', 'message')



