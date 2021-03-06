import json
from django.http import Http404, HttpResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.detail import DetailView
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import get_object_or_404
from .models import Alert, WebhookData
from .forms import AlertCreateForm
from .blockset import get_blockchains


class CreateAlertView(CreateView):
    form_class = AlertCreateForm
    template_name = 'create.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['blockchains'] = get_blockchains()
        return context

    def get_success_url(self):
        return reverse_lazy('alert_create_success')


class SuccessView(TemplateView):
    template_name = 'success.html'


class ConfirmView(DetailView):
    template_name = 'confirm.html'
    queryset = Alert.objects.filter()

    def get(self, request, *args, **kwargs):
        resp = super().get(request, *args, **kwargs)
        if str(self.object.token) != request.GET.get('token', ''):
            raise Http404(_('Alert not found'))
        if not self.object.active:
            self.object.activate(request)
        return resp


class DeactivateView(DetailView):
    template_name = 'deactivate.html'
    queryset = Alert.objects.filter()

    def get(self, request, *args, **kwargs):
        resp = super().get(request, *args, **kwargs)
        if str(self.object.token) != request.GET.get('token', ''):
            raise Http404(_('Alert not found'))
        if self.object.active:
            self.object.deactivate()
        return resp


class WebhookView(DetailView):
    queryset = Alert.objects.filter()

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        instance = self.get_object()
        if str(instance.token) != request.GET.get('token', '') or not instance.active:
            raise Http404(_('Alert not found'))
        hook_data = json.loads(request.body.decode('utf-8'))
        webhook = WebhookData(alert=instance, body=hook_data)
        webhook.save()
        webhook.send_email(request)
        return HttpResponse(status=204)


class WebhookDetailView(DetailView):
    template_name = 'webhook.html'

    def get_object(self, queryset=None):
        alert = get_object_or_404(Alert, pk=self.kwargs['alertpk'])
        if str(alert.token) != self.request.GET.get('token', ''):
            raise Http404(_('Alert not found'))
        webhook = get_object_or_404(WebhookData, alert=alert, pk=self.kwargs['webhookpk'])
        return webhook
