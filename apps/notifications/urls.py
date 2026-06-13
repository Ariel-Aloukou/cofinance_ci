# apps/notifications/urls.py

from django.urls import path
from .views import (
    NotificationListView,
    MarquerLuView,
    ToutMarquerLuView,
)

urlpatterns = [
    path("",                NotificationListView.as_view(),  name="notification-list"),
    path("<int:pk>/lire/",  MarquerLuView.as_view(),         name="notification-lire"),
    path("tout-lire/",      ToutMarquerLuView.as_view(),     name="notification-tout-lire"),
]