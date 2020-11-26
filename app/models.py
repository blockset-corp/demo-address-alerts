import uuid
from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.conf import settings
from django.urls import reverse_lazy
from django.contrib.postgres import fields as pgfields
from django.contrib.postgres import indexes as pgindexes
from django.core.mail import send_mail
from django.template.loader import render_to_string
from .blockset import create_subscription, delete_subscription


class Alert(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    token = models.UUIDField(default=uuid.uuid4)
    email = models.EmailField()
    addresses = pgfields.ArrayField(models.CharField(max_length=255), size=100)
    active = models.BooleanField(default=False)
    subscription_id = models.CharField(default='', max_length=255)

    class Meta:
        indexes = [
            pgindexes.GinIndex(fields=('addresses',), name='active_addresses')
        ]

    def __str__(self):
        return self.email

    def activate(self, request):
        self.active = True
        url = request.build_absolute_uri(reverse_lazy('alert_webhook', kwargs={'pk': self.id})) + f'?token={self.token}'
        subscription = create_subscription(url, self.addresses)
        print(f'subscription {subscription}')
        self.subscription_id = subscription['subscription_id']
        self.save()


class WebhookData(models.Model):
    alert = models.ForeignKey(Alert, on_delete=models.CASCADE)
    received = models.DateTimeField(auto_now_add=True)
    body = models.JSONField()

    class Meta:
        ordering = ('-received',)
        verbose_name = 'Webhook'
        verbose_name_plural = 'Webhooks'
        indexes = [
            models.Index(fields=('alert_id', 'received'), name='alert_by_received')
        ]

    def __str__(self):
        return str(self.alert)

    def send_email(self):
        context = {
            'webhook': self
        }
        send_mail(
            subject=render_to_string('emails/alert_subject.html', context=context),
            message=render_to_string('emails/alert_message.html', context=context),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[self.alert.email]
        )


class Block(models.Model):
    email = models.EmailField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


@receiver(pre_delete, sender=Alert)
def remove_subscription(sender, instance, *args, **kwargs):
    if len(instance.subscription_id) > 0:
        try:
            delete_subscription(instance.subscription_id)
        except Exception as e:
            print(f'error deleting subscription {e}')
