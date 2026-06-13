# apps/assurance/urls.py

from django.urls import path
from .views import (
    FormulaListView,
    FormulaDetailView,
    SouscriptionCreateView,
    MesSouscriptionsView,
    SouscriptionDetailView,
)

urlpatterns = [
    path("formules/",              FormulaListView.as_view(),         name="formule-list"),
    path("formules/<int:pk>/",     FormulaDetailView.as_view(),       name="formule-detail"),
    path("souscriptions/",         SouscriptionCreateView.as_view(),  name="souscription-create"),
    path("mes-souscriptions/",     MesSouscriptionsView.as_view(),    name="souscription-list"),
    path("souscriptions/<int:pk>/", SouscriptionDetailView.as_view(), name="souscription-detail"),
]