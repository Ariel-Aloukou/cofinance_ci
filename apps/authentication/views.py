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
 
 
@extend_schema(
    tags=["Chat"],
    summary="Assigner manuellement un agent à une conversation",
)
class AssignerAgentView(APIView):
    permission_classes = [EstAdmin]
 
    def patch(self, request, pk):
        from .serializers import AssignationManuelleSerializer
        from django.contrib.auth import get_user_model
        from .models import Conversation
 
        try:
            conversation = Conversation.objects.get(pk=pk)
        except Conversation.DoesNotExist:
            return Response({"error": "Conversation introuvable."}, status=404)
 
        serializer = AssignationManuelleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
 
        User  = get_user_model()
        agent = User.objects.get(pk=serializer.validated_data["agent_id"])
 
        conversation.agent  = agent
        conversation.statut = "EN_COURS"
        conversation.save()
 
        return Response({
            "message": f"Agent {agent.get_full_name()} assigné avec succès.",
            "conversation_id": conversation.id,
            "agent_id": agent.id,
        })
 
 
@extend_schema(
    tags=["Chat"],
    summary="Fermer une conversation et libérer l'agent",
)
class FermerConversationView(APIView):
    permission_classes = [EstAgent]
 
    def patch(self, request, pk):
        from .models import Conversation
        from .services import liberer_agent
 
        try:
            conversation = Conversation.objects.get(pk=pk)
        except Conversation.DoesNotExist:
            return Response({"error": "Conversation introuvable."}, status=404)
 
        conversation.statut = "FERMEE"
        conversation.save()
        liberer_agent(conversation)
 
        return Response({"message": "Conversation fermée.", "statut": "FERMEE"})
