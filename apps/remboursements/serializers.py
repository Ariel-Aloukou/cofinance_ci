# apps/remboursements/serializers.py

from rest_framework import serializers
from .models import Paiement
from apps.credits.models import EcheancierRemboursement
from apps.remboursements.models import Paiement


class PaiementSerializer(serializers.ModelSerializer):
    client_nom      = serializers.CharField(
        source="echeance.demande.client.get_full_name",
        read_only=True,
    )
    agent_nom       = serializers.CharField(
        source="agent.get_full_name",
        read_only=True,
    )
    date_echeance   = serializers.DateField(
        source="echeance.date_echeance",
        read_only=True,
    )
    montant_echeance = serializers.DecimalField(
        source="echeance.montant_total",
        max_digits=12, decimal_places=2,
        read_only=True,
    )

    class Meta:
        model  = Paiement
        fields = [
            "id", "echeance", "date_echeance", "montant_echeance",
            "agent", "agent_nom", "client_nom",
            "montant_paye", "penalite_retard",
            "moyen_paiement", "reference_transaction",
            "date_paiement", "commentaire",
        ]
        read_only_fields = [
            "agent", "penalite_retard", "date_paiement",
        ]

    def validate_echeance(self, value):
        """Vérifie que l'échéance n'est pas déjà payée."""
        if value.est_paye:
            raise serializers.ValidationError(
                "Cette échéance a déjà été payée."
            )
        return value


class AlerteEcheanceSerializer(serializers.ModelSerializer):
    """Sérialise une échéance pour les alertes J-3 / J+1."""
    client_nom    = serializers.CharField(
        source="demande.client.get_full_name",
        read_only=True,
    )
    client_tel    = serializers.CharField(
        source="demande.client.telephone",
        read_only=True,
    )
    client_region = serializers.CharField(
        source="demande.client.region",
        read_only=True,
    )
    jours_restants = serializers.SerializerMethodField()

    class Meta:
        model  = EcheancierRemboursement
        fields = [
            "id", "demande", "client_nom", "client_tel", "client_region",
            "numero_echeance", "date_echeance",
            "montant_total", "jours_restants",
        ]

    def get_jours_restants(self, obj):
        from datetime import date
        delta = obj.date_echeance - date.today()
        return delta.days