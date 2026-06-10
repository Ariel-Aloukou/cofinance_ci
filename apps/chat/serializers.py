# apps/chat/serializers.py

from rest_framework import serializers
from .models import Conversation, Message, EvaluationConversation


class MessageSerializer(serializers.ModelSerializer):
    auteur_nom = serializers.CharField(
        source="auteur.get_full_name",
        read_only=True,
    )

    class Meta:
        model  = Message
        fields = [
            "id", "conversation", "auteur", "auteur_nom",
            "contenu", "est_lu", "created_at",
        ]
        read_only_fields = ["auteur", "created_at"]


class ConversationSerializer(serializers.ModelSerializer):
    client_nom  = serializers.CharField(
        source="client.get_full_name",
        read_only=True,
    )
    agent_nom   = serializers.CharField(
        source="agent.get_full_name",
        read_only=True,
    )
    nb_messages = serializers.SerializerMethodField()

    class Meta:
        model  = Conversation
        fields = [
            "id", "client", "client_nom",
            "agent", "agent_nom",
            "sujet", "statut",
            "nb_messages", "created_at", "updated_at",
        ]
        read_only_fields = [
            "client", "agent", "statut",
            "created_at", "updated_at",
        ]

    def get_nb_messages(self, obj):
        return obj.messages.count()


class AssignationManuelleSerializer(serializers.Serializer):
    """Valide l'assignation manuelle d'un agent à une conversation."""
    agent_id = serializers.IntegerField()

    def validate_agent_id(self, value):
        from django.contrib.auth import get_user_model
        User = get_user_model()
        try:
            User.objects.get(pk=value, role__in=["AGENT", "ADMIN"])
        except User.DoesNotExist:
            raise serializers.ValidationError("Agent introuvable.")
        return value


class EvaluationSerializer(serializers.ModelSerializer):
    class Meta:
        model  = EvaluationConversation
        fields = [
            "id", "conversation",
            "note_nps", "note_satisfaction",
            "commentaire", "created_at",
        ]
        read_only_fields = ["client", "created_at"]

    def validate_note_nps(self, value):
        if not 0 <= value <= 10:
            raise serializers.ValidationError(
                "La note NPS doit être entre 0 et 10."
            )
        return value

    def validate_note_satisfaction(self, value):
        if not 1 <= value <= 5:
            raise serializers.ValidationError(
                "La note de satisfaction doit être entre 1 et 5."
            )
        return value

    def validate_conversation(self, value):
        if value.statut != "FERMEE":
            raise serializers.ValidationError(
                "Vous ne pouvez évaluer qu'une conversation fermée."
            )
        if hasattr(value, "evaluation"):
            raise serializers.ValidationError(
                "Cette conversation a déjà été évaluée."
            )
        return value