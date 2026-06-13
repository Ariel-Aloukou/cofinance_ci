# apps/remboursements/views.py

from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema

from .models import Paiement
from .serializers import PaiementSerializer, AlerteEcheanceSerializer
from .services import calculer_penalite_retard, obtenir_alertes
from apps.authentication.permissions import EstAgent
from apps.notifications.models import Notification


# ─────────────────────────────────────────────────────────────────────
# ENREGISTRER UN PAIEMENT
# ─────────────────────────────────────────────────────────────────────

@extend_schema(
    tags=["Remboursements"],
    summary="Enregistrer un paiement",
    description=(
        "Enregistre le paiement d'une échéance par un agent. "
        "Calcule automatiquement les pénalités de retard si applicable. "
        "Marque l'échéance comme payée et notifie le client."
    ),
)
class EnregistrerPaiementView(generics.CreateAPIView):
    """
    Seuls les agents et admins peuvent enregistrer un paiement.
    """
    serializer_class   = PaiementSerializer
    permission_classes = [EstAgent]

    def perform_create(self, serializer):
        echeance = serializer.validated_data["echeance"]

        # Calcul automatique de la pénalité de retard
        penalite = calculer_penalite_retard(echeance)

        # Enregistrement du paiement
        paiement = serializer.save(
            agent=self.request.user,
            penalite_retard=penalite,
        )

        # Marquer l'échéance comme payée
        from datetime import date
        echeance.est_paye               = True
        echeance.date_paiement_effectif = date.today()
        echeance.save()

        # Notifier le client
        Notification.objects.create(
            destinataire      = echeance.demande.client,
            type_notification = "REMBOURSEMENT",
            titre             = "Paiement enregistré",
            message           = (
                f"Votre paiement de {paiement.montant_paye} FCFA "
                f"a été enregistré pour l'échéance "
                f"#{echeance.numero_echeance}."
            ),
        )


# ─────────────────────────────────────────────────────────────────────
# HISTORIQUE DES PAIEMENTS
# ─────────────────────────────────────────────────────────────────────

@extend_schema(
    tags=["Remboursements"],
    summary="Historique des paiements",
    description=(
        "Retourne la liste des paiements. "
        "Un client voit uniquement ses propres paiements. "
        "Un agent voit les paiements qu'il a enregistrés. "
        "Un admin voit tout."
    ),
)
class HistoriquePaiementsView(generics.ListAPIView):
    serializer_class   = PaiementSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.role == "CLIENT":
            return Paiement.objects.filter(
                echeance__demande__client=user
            ).order_by("-date_paiement")

        if user.role == "AGENT":
            return Paiement.objects.filter(
                agent=user
            ).order_by("-date_paiement")

        # ADMIN — tout voir
        return Paiement.objects.all().order_by("-date_paiement")


# ─────────────────────────────────────────────────────────────────────
# ALERTES J-3 / J+1
# ─────────────────────────────────────────────────────────────────────

@extend_schema(
    tags=["Remboursements"],
    summary="Alertes échéances J-3 et J+1",
    description=(
        "Retourne deux listes :\n"
        "- **echeances_a_venir_j3** : échéances dues dans 3 jours\n"
        "- **echeances_en_retard_j1** : échéances en retard d'un jour\n"
        "Réservé aux agents et administrateurs."
    ),
)
class AlertesView(APIView):
    permission_classes = [EstAgent]

    def get(self, request):
        alertes_a_venir, alertes_retard = obtenir_alertes()

        return Response({
            "echeances_a_venir_j3": AlerteEcheanceSerializer(
                alertes_a_venir, many=True
            ).data,
            "echeances_en_retard_j1": AlerteEcheanceSerializer(
                alertes_retard, many=True
            ).data,
        })