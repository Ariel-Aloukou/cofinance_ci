# apps/notifications/admin.py
from django.contrib import admin
from .models import Notification

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display  = ['destinataire', 'type_notification',
                     'titre', 'est_lu', 'created_at']
    list_filter   = ['type_notification', 'est_lu']
    search_fields = ['titre', 'destinataire__username']