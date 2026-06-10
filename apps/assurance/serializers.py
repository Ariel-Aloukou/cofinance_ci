# apps/assurance/serializers.py

from rest_framework import serializers
from .models import FormulaAssurance, Souscription


class FormulaAssuranceSerializer(serializers.ModelSerializer):
    class Meta:
        model  = FormulaAssurance
        fields = [
            "id", "nom", "categorie", "description",
            "prime_mensuelle", "capital_garanti",
            "duree_mois", "est_active",
        ]
        read_only_fields = fields


class SouscriptionSerializer(serializers.ModelSerializer):
    client_nom   = serializers.CharField(
        source="client.get_full_name",
        read_only=True,
    )
    formule_nom  = serializers.CharField(
        source="formule.nom",
        read_only=True,
    )
    jours_avant_expiration = serializers.SerializerMethodField()

    class Meta:
        model  = Souscription
        fields = [
            "id", "client", "client_nom",
            "formule", "formule_nom",
            "statut", "date_souscription", "date_expiration",
            "jours_avant_expiration",
        ]
        read_only_fields = [
            "client", "statut",
            "date_souscription", "date_expiration",
        ]

    def get_jours_avant_expiration(self, obj):
        from datetime import date
        delta = obj.date_expiration - date.today()
        return delta.days