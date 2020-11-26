from django.contrib import admin
from .models import Alert, Block, WebhookData


@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    pass


@admin.register(Block)
class BlockAdmin(admin.ModelAdmin):
    pass


@admin.register(WebhookData)
class WebhookDataAdmin(admin.ModelAdmin):
    pass
