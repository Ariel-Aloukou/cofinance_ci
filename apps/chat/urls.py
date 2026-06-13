# apps/chat/urls.py

from django.urls import path
from .views import (
    ConversationListCreateView,
    HistoriqueMessagesView,
    AssignerAgentView,
    FermerConversationView,
    SoumettreEvaluationView,
    ResultatsNPSView,
)

urlpatterns = [
    # Conversations
    path("conversations/",
         ConversationListCreateView.as_view(),
         name="conversation-list"),

    # Messages d'une conversation  ← celle qui manque
    path("conversations/<int:pk>/messages/",
         HistoriqueMessagesView.as_view(),
         name="conversation-messages"),

    # Assignation manuelle d'un agent
    path("conversations/<int:pk>/assigner/",
         AssignerAgentView.as_view(),
         name="chat-assigner"),

    # Fermer une conversation
    path("conversations/<int:pk>/fermer/",
         FermerConversationView.as_view(),
         name="chat-fermer"),

    # Évaluations NPS
    path("evaluations/",
         SoumettreEvaluationView.as_view(),
         name="chat-evaluation"),

    path("nps/",
         ResultatsNPSView.as_view(),
         name="chat-nps"),
]