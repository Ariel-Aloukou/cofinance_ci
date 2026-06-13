# apps/credits/views.py

from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import generics, permissions
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.exceptions import ValidationError as DRFValidationError
from drf_spectacular.utils import extend_schema

# Modèles
from apps.credits.models import (
    DemandeCredit,
    HistoriqueStatutCredit,
    PieceJustificative,
    EcheancierRemboursement,
)

# Serializers — à créer dans serializers.py (voir ci-dessous)
from apps.credits.serializers import (
    DemandeCreditSerializer,
    ChangerStatutSerializer,
    HistoriqueStatutSerializer,
    PieceJustificativeSerializer,
    EcheancierSerializer,
)

# Services
from .services import (
    calculer_score_eligibilite,
    generer_echeancier,
    changer_statut_avec_historique,
)

# Permissions
from apps.authentication.permissions import EstAgent

# Notifications
from apps.notifications.models import Notification


# ─────────────────────────────────────────────────────────────────────
# MODULE CRÉDITS
# ─────────────────────────────────────────────────────────────────────

@extend_schema(tags=["Microcrédits"])
class DemandeCreditViewSet(ModelViewSet):
    serializer_class   = DemandeCreditSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == "CLIENT":
            return DemandeCredit.objects.filter(client=user)
        if user.role == "AGENT":
            return DemandeCredit.objects.filter(agent_traitant=user)
        return DemandeCredit.objects.all()  # ADMIN

    def perform_create(self, serializer):
        demande = serializer.save(client=self.request.user)
        demande.score_eligibilite = calculer_score_eligibilite(
            self.request.user,
            demande.montant_demande,
            demande.duree_mois,
        )
        demande.save()

    # ── Action 1 : Changer le statut ──────────────────────────────
    @extend_schema(
        tags=["Microcrédits"],
        summary="Changer le statut d'une demande (workflow validé)",
        description=(
            "Transitions autorisées :\n"
            "- SOUMISE → EN_ANALYSE ou REJETEE\n"
            "- EN_ANALYSE → APPROUVEE ou REJETEE\n"
            "- APPROUVEE → DECAISSEE ou REJETEE\n"
            "Toute autre transition est refusée avec une erreur 400."
        ),
    )
    @action(
        detail=True,
        methods=["patch"],
        url_path="statut",
        permission_classes=[EstAgent],
    )
    def changer_statut(self, request, pk=None):
        demande    = self.get_object()
        serializer = ChangerStatutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        nouveau_statut   = serializer.validated_data["statut"]
        commentaire      = serializer.validated_data.get("commentaire_agent", "")
        montant_approuve = serializer.validated_data.get("montant_approuve")

        if montant_approuve and nouveau_statut == "APPROUVEE":
            demande.montant_approuve = montant_approuve
            demande.save()

        try:
            demande = changer_statut_avec_historique(
                demande, nouveau_statut, request.user, commentaire
            )
        except ValueError as e:
            raise DRFValidationError({"statut": str(e)})

        return Response(DemandeCreditSerializer(demande).data)

    # ── Action 2 : Voir l'échéancier ──────────────────────────────
    @extend_schema(
        tags=["Microcrédits"],
        summary="Voir l'échéancier de remboursement d'une demande",
    )
    @action(
        detail=True,
        methods=["get"],
        url_path="echeancier",
    )
    def echeancier(self, request, pk=None):
        demande   = self.get_object()
        echeances = demande.echeances.all()
        return Response(EcheancierSerializer(echeances, many=True).data)

    # ── Action 3 : Historique des statuts ─────────────────────────
    @extend_schema(
        tags=["Microcrédits"],
        summary="Historique des changements de statut d'une demande",
    )
    @action(
        detail=True,
        methods=["get"],
        url_path="historique",
    )
    def historique(self, request, pk=None):
        demande    = self.get_object()
        historique = demande.historique_statuts.all()
        return Response(
            HistoriqueStatutSerializer(historique, many=True).data
        )


# ─────────────────────────────────────────────────────────────────────
# MODULE PIÈCES JUSTIFICATIVES
# ─────────────────────────────────────────────────────────────────────

@extend_schema(
    tags=["Pièces Justificatives"],
    summary="Uploader une pièce justificative",
    description=(
        "Upload d'un fichier pour une demande de crédit. "
        "Formats acceptés : PDF, JPG, PNG. Taille max : 10 Mo."
    ),
)
class PieceJustificativeUploadView(generics.CreateAPIView):
    serializer_class   = PieceJustificativeSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes     = [MultiPartParser, FormParser]

    def perform_create(self, serializer):
        serializer.save(uploaded_by=self.request.user)


@extend_schema(
    tags=["Pièces Justificatives"],
    summary="Lister les pièces justificatives d'une demande",
)
class PieceJustificativeListView(generics.ListAPIView):
    serializer_class   = PieceJustificativeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        demande_id = self.kwargs["demande_id"]
        return PieceJustificative.objects.filter(demande_id=demande_id)


@extend_schema(
    tags=["Pièces Justificatives"],
    summary="Supprimer une pièce justificative",
)
class PieceJustificativeDeleteView(generics.DestroyAPIView):
    serializer_class   = PieceJustificativeSerializer
    permission_classes = [permissions.IsAuthenticated]
   