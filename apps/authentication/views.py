from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions
from rest_framework_simplejwt.views import TokenObtainPairView
# Remplace ton import actuel de drf_spectacular par celui-ci
from drf_spectacular.utils import (
    extend_schema,
    OpenApiParameter,
    OpenApiExample,
    OpenApiResponse,
)
from .serializers import InscriptionSerializer, ProfilSerializer
from apps.authentication.permissions import EstAdmin, EstAgent, EstClient
from .models import PresenceAgent
from .serializers import PresenceAgentSerializer
from rest_framework.views import APIView
from rest_framework.response import Response


 
@extend_schema(
    tags=["Authentification"],
    summary="Inscription d'un nouveau client",
    description="""
Crée un nouveau compte utilisateur avec le rôle CLIENT.
Ne nécessite pas d'authentification.
Le nom d'utilisateur doit être unique.
    """,
    responses={
        201: InscriptionSerializer,
        400: OpenApiResponse(description="Données invalides (ex: mots de passe différents)"),
    },
    examples=[
        OpenApiExample(
            name="Inscription client",
            value={
                "username":       "nouveau_client",
                "email":          "client@gmail.com",
                "first_name":     "Amara",
                "last_name":      "TRAORÉ",
                "telephone":      "+225 07 00 11 22",
                "region":         "Adjamé",
                "password":       "MonMotDePasse@2026",
                "password2":      "MonMotDePasse@2026",
            },
            request_only=True,
        ),
        OpenApiExample(
            name="Réponse succès",
            value={
                "username": "nouveau_client",
                "email":    "client@gmail.com",
                "role":     "CLIENT",
            },
            response_only=True,
            status_codes=["201"],
        ),
    ]
)
class InscriptionView(generics.CreateAPIView):
    serializer_class   = InscriptionSerializer
    permission_classes = [permissions.AllowAny]
 
@extend_schema(tags=["Authentification"], summary="Connexion JWT")
class LoginView(TokenObtainPairView):
    pass
 
@extend_schema(tags=["Authentification"], summary="Profil utilisateur")
class ProfilView(generics.RetrieveUpdateAPIView):
    serializer_class   = ProfilSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_object(self): return self.request.user

@extend_schema(
    tags=["Présence Agents"],
    summary="Liste des agents et leur statut de présence",
)
class PresenceAgentListView(generics.ListAPIView):
    """Voir quels agents sont en ligne — réservé aux admins."""
    serializer_class   = PresenceAgentSerializer
    permission_classes = [EstAdmin]
    queryset           = PresenceAgent.objects.select_related("agent").all()
 
 
@extend_schema(
    tags=["Présence Agents"],
    summary="Mettre à jour son propre statut de disponibilité",
)
class MettreAJourPresenceView(generics.UpdateAPIView):
    """
    Un agent met à jour son propre statut :
    DISPONIBLE, OCCUPE, ABSENT.
    """
    serializer_class   = PresenceAgentSerializer
    permission_classes = [EstAgent]
 
    def get_object(self):
        # Crée la présence si elle n'existe pas encore
        presence, _ = PresenceAgent.objects.get_or_create(
            agent=self.request.user
        )
        return presence
 
 

