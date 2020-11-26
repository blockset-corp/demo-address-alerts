from django.urls import path
from .views import CreateAlertView, SuccessView, ConfirmView, DeactivateView, \
    WebhookView, WebhookDetailView

urlpatterns = [
    path('', CreateAlertView.as_view(), name='alert_create'),
    path('success/', SuccessView.as_view(), name='alert_create_success'),
    path('<int:pk>/confirm/', ConfirmView.as_view(), name='alert_confirm'),
    path('<int:pk>/deactivate/', DeactivateView.as_view(), name='alert_deactivate'),
    path('<int:pk>/webhook/', WebhookView.as_view(), name='alert_webhook'),
    path('<int:alertpk>/webhook/<int:webhookpk>/', WebhookDetailView.as_view(), name='alert_webhook_detail'),
]
