from django.urls import path
from .views import CreateAlertView, SuccessView, ConfirmView, WebhookView

urlpatterns = [
    path('', CreateAlertView.as_view(), name='alert_create'),
    path('success/', SuccessView.as_view(), name='alert_create_success'),
    path('<int:pk>/confirm/', ConfirmView.as_view(), name='alert_confirm'),
    path('<int:pk>/webhook/', WebhookView.as_view(), name='alert_webhook'),
]
