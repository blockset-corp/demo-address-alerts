from django import forms
from django.conf import settings
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
from .models import Alert


class AlertCreateForm(forms.ModelForm):
    email = forms.EmailField(required=True,
                             help_text=_('You will be required to confirm this email'))
    addresses = forms.CharField(required=True, widget=forms.HiddenInput)

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request

    class Meta:
        model = Alert
        fields = ('email', 'addresses')

    def save(self, commit=True):
        instance = super().save(commit=commit)
        confirm_url = self.request.build_absolute_uri(reverse_lazy('alert_confirm', kwargs={'pk': instance.pk})
                                                      + f'?token={instance.token}')
        context = {
            'alert': instance,
            'confirm_url': confirm_url
        }
        send_mail(
            subject=render_to_string('emails/confirm_subject.html', context=context, request=self.request),
            message=render_to_string('emails/confirm_message.html', context=context, request=self.request),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[instance.email]
        )
        return instance
