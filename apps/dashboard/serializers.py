# apps/dashboard/serializers.py

from rest_framework import serializers


class StatsGlobalesSerializer(serializers.Serializer):
    """
    Sérialise la réponse du tableau de bord.
    Pas de modèle associé — ce sont des données calculées.
    """
    filtres_appliques             = serializers.DictField()
    credits_par_statut            = serializers.DictField()
    montant_total_decaisse_fcfa   = serializers.FloatField()
    taux_recouvrement_pct         = serializers.FloatField()
    souscriptions_actives         = serializers.IntegerField()
    conversations_ouvertes        = serializers.IntegerField()
    conversations_non_traitees    = serializers.IntegerField()
    date_calcul                   = serializers.DateTimeField()


class ConversationEnAttenteSerializer(serializers.Serializer):
    """Sérialise une conversation en attente d'agent."""
    id               = serializers.IntegerField()
    client_nom       = serializers.CharField()
    client_region    = serializers.CharField()
    sujet            = serializers.CharField()
    attente_minutes  = serializers.IntegerField()
    created_at       = serializers.DateTimeField()