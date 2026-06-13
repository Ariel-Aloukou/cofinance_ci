# apps/dashboard/urls.py

from django.urls import path
from .views import (
    StatsGlobalesView,
    ConversationsNonTraiteesView,
)

urlpatterns = [
    path("stats/",
         StatsGlobalesView.as_view(),
         name="dashboard-stats"),

    path("conversations-en-attente/",
         ConversationsNonTraiteesView.as_view(),
         name="dashboard-conversations-attente"),
]