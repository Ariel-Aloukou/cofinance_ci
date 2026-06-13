# apps/credits/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    DemandeCreditViewSet,
    PieceJustificativeUploadView,
    PieceJustificativeListView,
    PieceJustificativeDeleteView,
)

# Le router génère automatiquement les routes CRUD du ViewSet
router = DefaultRouter()
router.register("demandes", DemandeCreditViewSet, basename="demande-credit")

urlpatterns = [
    # Routes CRUD + actions (statut, echeancier, historique)
    path("", include(router.urls)),

    # Pièces justificatives
    path("demandes/<int:demande_id>/pieces/",
         PieceJustificativeListView.as_view(),
         name="pieces-list"),

    path("demandes/<int:demande_id>/pieces/upload/",
         PieceJustificativeUploadView.as_view(),
         name="pieces-upload"),

    path("pieces/<int:pk>/",
         PieceJustificativeDeleteView.as_view(),
         name="pieces-delete"),
]