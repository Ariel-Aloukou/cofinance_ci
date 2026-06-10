from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions
from drf_spectacular.utils import extend_schema
from apps.authentication.permissions import EstAdmin, EstAgent, EstClient
from apps.chat.services import assigner_agent_automatiquement
from apps.chat.models import Conversation, Message
from apps.chat.serializers import (
    ConversationSerializer,
    MessageSerializer
)
from rest_framework.views import APIView
from rest_framework.response import Response
from apps.chat.serializers import (
    EvaluationSerializer,
)



@extend_schema(tags=["Chat"])
class ConversationListCreateView(generics.ListCreateAPIView):
    serializer_class   = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]
 
    def get_queryset(self):
        user = self.request.user
        if user.role == "CLIENT": return Conversation.objects.filter(client=user)
        return Conversation.objects.all()
 
    def perform_create(self, serializer):
        """
        Crée la conversation ET tente une assignation automatique
        si un agent est disponible.
        """
        conversation = serializer.save(client=self.request.user)
        assigner_agent_automatiquement(conversation)

 
@extend_schema(tags=["Chat"])
class HistoriqueMessagesView(generics.ListAPIView):
    serializer_class   = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]
 
    def get_queryset(self):
        return Message.objects.filter(conversation_id=self.kwargs["pk"])
    
 
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

@extend_schema(
    tags=["Chat — Évaluation"],
    summary="Soumettre une évaluation après une conversation",
    description="Note NPS (0-10) + satisfaction (1-5) après fermeture de la conversation.",
)
class SoumettreEvaluationView(generics.CreateAPIView):
    serializer_class   = EvaluationSerializer
    permission_classes = [EstClient]
 
    def perform_create(self, serializer):
        serializer.save(client=self.request.user)
 
 
@extend_schema(
    tags=["Chat — Évaluation"],
    summary="Résultats NPS et satisfaction globale",
)
class ResultatsNPSView(APIView):
    permission_classes = [EstAdmin]
 
    def get(self, request):
        from .services import calculer_nps
        from .models import EvaluationConversation
        from django.db.models import Avg
 
        nps_data = calculer_nps()
        satisfaction_moyenne = EvaluationConversation.objects.aggregate(
            Avg("note_satisfaction")
        )["note_satisfaction__avg"] or 0
 
        return Response({
            **nps_data,
            "satisfaction_moyenne": round(float(satisfaction_moyenne), 2),
        })
