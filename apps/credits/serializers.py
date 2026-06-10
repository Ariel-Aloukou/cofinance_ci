# apps/credits/serializers.py

from rest_framework import serializers
from .models import (
    DemandeCredit,
    EcheancierRemboursement,
    HistoriqueStatutCredit,
    PieceJustificative,
)


class EcheancierSerializer(serializers.ModelSerializer):
    class Meta:
        model  = EcheancierRemboursement
        fields = [
            "id", "demande", "numero_echeance", "date_echeance",
            "montant_capital", "montant_interet", "montant_total",
            "est_paye", "date_paiement_effectif",
        ]
        read_only_fields = fields


class HistoriqueStatutSerializer(serializers.ModelSerializer):
    modifie_par_nom        = serializers.CharField(
        source="modifie_par.get_full_name",
        read_only=True,
    )
    statut_precedent_label = serializers.CharField(
        source="get_statut_precedent_display",
        read_only=True,
    )
    nouveau_statut_label   = serializers.CharField(
        source="get_nouveau_statut_display",
        read_only=True,
    )

    class Meta:
        model  = HistoriqueStatutCredit
        fields = [
            "id", "statut_precedent", "statut_precedent_label",
            "nouveau_statut", "nouveau_statut_label",
            "modifie_par", "modifie_par_nom",
            "commentaire", "created_at",
        ]
        read_only_fields = fields


class DemandeCreditSerializer(serializers.ModelSerializer):
    client_nom = serializers.CharField(
        source="client.get_full_name",
        read_only=True,
    )
    echeances  = EcheancierSerializer(many=True, read_only=True)

    class Meta:
        model  = DemandeCredit
        fields = [
            "id", "client", "client_nom", "agent_traitant",
            "montant_demande", "duree_mois", "periodicite",
            "taux_interet_annuel", "objet_credit",
            "statut", "score_eligibilite",
            "montant_approuve", "commentaire_agent",
            "date_soumission", "date_approbation", "date_decaissement",
            "echeances",
        ]
        read_only_fields = [
            "client", "statut", "score_eligibilite",
            "date_soumission", "date_approbation", "date_decaissement",
        ]


class ChangerStatutSerializer(serializers.Serializer):
    """Valide le changement de statut d'une demande de crédit."""
    statut           = serializers.ChoiceField(
        choices=DemandeCredit.STATUT_CHOICES,
    )
    montant_approuve = serializers.DecimalField(
        max_digits=12, decimal_places=2, required=False,
    )
    commentaire_agent = serializers.CharField(required=False, default="")


class PieceJustificativeSerializer(serializers.ModelSerializer):
    url_telechargement = serializers.SerializerMethodField()

    class Meta:
        model  = PieceJustificative
        fields = [
            "id", "demande", "type_document", "fichier",
            "nom_original", "taille_octets", "uploaded_by",
            "created_at", "url_telechargement",
        ]
        read_only_fields = [
            "nom_original", "taille_octets",
            "uploaded_by", "created_at",
        ]

    def get_url_telechargement(self, obj):
        request = self.context.get("request")
        if obj.fichier and request:
            return request.build_absolute_uri(obj.fichier.url)
        return None

    def validate_fichier(self, value):
        import os
        extensions_autorisees = [".pdf", ".jpg", ".jpeg", ".png"]
        taille_max = 10 * 1024 * 1024  # 10 Mo
        ext = os.path.splitext(value.name)[1].lower()
        if ext not in extensions_autorisees:
            raise serializers.ValidationError(
                f"Format non autorisé. Acceptés : {extensions_autorisees}"
            )
        if value.size > taille_max:
            raise serializers.ValidationError(
                "Fichier trop volumineux (max 10 Mo)."
            )
        return value