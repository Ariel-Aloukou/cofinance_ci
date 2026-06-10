# apps/authentication/serializers.py

from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import CustomUser, PresenceAgent  # ← PresenceAgent ajouté


# ─────────────────────────────────────────────────────────────────────
# INSCRIPTION
# ─────────────────────────────────────────────────────────────────────

class InscriptionSerializer(serializers.ModelSerializer):
    password  = serializers.CharField(
        write_only=True,
        validators=[validate_password],
    )
    password2 = serializers.CharField(
        write_only=True,
        label="Confirmer le mot de passe",
    )

    class Meta:
        model  = CustomUser
        fields = [
            "username", "email", "first_name", "last_name",
            "telephone", "region", "date_naissance", "numero_cni",
            "password", "password2",
        ]

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                {"password": "Les mots de passe ne correspondent pas."}
            )
        return attrs

    def create(self, validated_data):
        validated_data.pop("password2")
        password = validated_data.pop("password")
        user = CustomUser(**validated_data, role="CLIENT")
        user.set_password(password)
        user.save()
        return user


# ─────────────────────────────────────────────────────────────────────
# PROFIL  (manquait dans ton fichier)
# ─────────────────────────────────────────────────────────────────────

class ProfilSerializer(serializers.ModelSerializer):
    class Meta:
        model  = CustomUser
        fields = [
            "id", "username", "email", "first_name", "last_name",
            "role", "telephone", "region", "adresse",
            "date_naissance", "numero_cni", "created_at",
        ]
        read_only_fields = ["id", "role", "username", "created_at"]


# ─────────────────────────────────────────────────────────────────────
# PRÉSENCE AGENT
# ─────────────────────────────────────────────────────────────────────

class PresenceAgentSerializer(serializers.ModelSerializer):
    agent_nom      = serializers.CharField(
        source="agent.get_full_name",
        read_only=True,
    )
    est_disponible = serializers.BooleanField(read_only=True)

    class Meta:
        model  = PresenceAgent
        fields = [
            "id", "agent", "agent_nom", "statut",
            "charge_courante", "capacite_max",
            "derniere_activite", "est_disponible",
        ]
        read_only_fields = ["agent", "charge_courante", "derniere_activite"]