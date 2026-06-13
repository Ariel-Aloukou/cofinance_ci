# apps/remboursements/urls.py

from django.urls import path
from .views import (
    EnregistrerPaiementView,
    HistoriquePaiementsView,
    AlertesView,
)

urlpatterns = [
    path("paiements/",   EnregistrerPaiementView.as_view(),  name="paiement-create"),
    path("historique/",  HistoriquePaiementsView.as_view(),  name="paiement-list"),
    path("alertes/",     AlertesView.as_view(),               name="alertes"),
]