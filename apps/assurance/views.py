# apps/assurance/views.py

from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from datetime import date
from dateutil.relativedelta import relativedelta

from .models import FormulaAssurance, Souscription
from .serializers import FormulaAssuranceSerializer, SouscriptionSerializer
from .services import verifier_expirations
from apps.authentication.permissions import EstClient, EstAdmin
from apps.notifications.models import Notification


# ─────────────────────────────────────────────────────────────────────
# CATALOGUE DES FORMULES
# ─────────────────────────────────────────────────────────────────────

@extend_schema(
    tags=["Assurance"],
    summary="Catalogue des formules d'assurance disponibles",
    description=(
        "Retourne toutes les formules d'assurance actives. "
        "Accessible à tous les utilisateurs authentifiés."
    ),
)
class FormulaListView(generics.ListAPIView):
    serializer_class   = FormulaAssuranceSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset           = FormulaAssurance.objects.filter(est_active=True)


# ─────────────────────────────────────────────────────────────────────
# DÉTAIL D'UNE FORMULE
# ─────────────────────────────────────────────────────────────────────

@extend_schema(
    tags=["Assurance"],
    summary="Détail d'une formule d'assurance",
)
class FormulaDetailView(generics.RetrieveAPIView):
    serializer_class   = FormulaAssuranceSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset           = FormulaAssurance.objects.filter(est_active=True)


# ─────────────────────────────────────────────────────────────────────
# SOUSCRIRE À UNE FORMULE
# ─────────────────────────────────────────────────────────────────────

@extend_schema(
    tags=["Assurance"],
    summary="Souscrire à une formule d'assurance",
    description=(
        "Permet à un client de souscrire à une formule d'assurance. "
        "La date d'expiration est calculée automatiquement "
        "selon la durée de la formule. "
        "Une notification de confirmation est envoyée au client."
    ),
)
class SouscriptionCreateView(generics.CreateAPIView):
    serializer_class   = SouscriptionSerializer
    permission_classes = [EstClient]

    def perform_create(self, serializer):
        formule = serializer.validated_data["formule"]

        # Calcul automatique de la date d'expiration
        date_expiration = date.today() + relativedelta(months=formule.duree_mois)

        souscription = serializer.save(
            client=self.request.user,
            date_expiration=date_expiration,
        )

        # Notification de confirmation au client
        Notification.objects.create(
            destinataire      = self.request.user,
            type_notification = "ASSURANCE",
            titre             = "Souscription confirmée",
            message           = (
                f"Votre souscription à \"{formule.nom}\" est active "
                f"jusqu'au {date_expiration.strftime('%d/%m/%Y')}. "
                f"Prime mensuelle : {formule.prime_mensuelle} FCFA."
            ),
        )


# ─────────────────────────────────────────────────────────────────────
# MES SOUSCRIPTIONS ACTIVES
# ─────────────────────────────────────────────────────────────────────

@extend_schema(
    tags=["Assurance"],
    summary="Mes polices d'assurance actives",
    description=(
        "Un client voit uniquement ses propres souscriptions actives. "
        "Un admin voit toutes les souscriptions actives."
    ),
)
class MesSouscriptionsView(generics.ListAPIView):
    serializer_class   = SouscriptionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == "CLIENT":
            return Souscription.objects.filter(
                client=user,
                statut="ACTIVE",
            ).select_related("formule")
        # AGENT et ADMIN voient tout
        return Souscription.objects.filter(
            statut="ACTIVE",
        ).select_related("client", "formule")


# ─────────────────────────────────────────────────────────────────────
# DÉTAIL D'UNE SOUSCRIPTION
# ─────────────────────────────────────────────────────────────────────

@extend_schema(
    tags=["Assurance"],
    summary="Détail d'une souscription",
)
class SouscriptionDetailView(generics.RetrieveAPIView):
    serializer_class   = SouscriptionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == "CLIENT":
            return Souscription.objects.filter(client=user)
        return Souscription.objects.all()


# ─────────────────────────────────────────────────────────────────────
# VÉRIFIER LES EXPIRATIONS (usage interne / admin)
# ─────────────────────────────────────────────────────────────────────

@extend_schema(
    tags=["Assurance"],
    summary="Déclencher la vérification des expirations à 15 jours",
    description=(
        "Envoie des notifications aux clients dont la souscription "
        "expire dans 15 jours. "
        "Réservé aux administrateurs. "
        "En production, cette route est appelée automatiquement "
        "par une tâche cron quotidienne."
    ),
)
class VerifierExpirationsView(APIView):
    permission_classes = [EstAdmin]

    def post(self, request):
        verifier_expirations()
        return Response({
            "message": "Vérification des expirations effectuée avec succès."
        })
        
@extend_schema(tags=["Assurance"], summary="Créer une formule (Admin)")
class FormulaCreateView(generics.CreateAPIView):
    serializer_class   = FormulaAssuranceSerializer
    permission_classes = [EstAdmin]        