from django.db import models
from django.conf import settings

from config.settings import AUTH_USER_MODEL

# Create your models here.
class Conversation(models.Model):
    STATUT_CHOICES = [("OUVERTE","Ouverte"),("EN_COURS","En cours"),("FERMEE","Fermée")]
    client     = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="conversations_client")
    agent      = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL, related_name="conversations_agent")
    sujet      = models.CharField(max_length=200, default="Support client")
    statut     = models.CharField(max_length=10, choices=STATUT_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
 
class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name="messages")
    auteur       = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="messages_auteur")
    contenu      = models.TextField()
    est_lu       = models.BooleanField(default=False)
    created_at   = models.DateTimeField(auto_now_add=True)

class EvaluationConversation(models.Model):
    """
    Évaluation de satisfaction laissée par un client
    après la fermeture d'une conversation.
    Utilisée pour calculer le NPS (Net Promoter Score).
    """
    # NPS : "Sur 10, recommanderiez-vous COFINANCE CI ?"
    # Détracteurs : 0-6 | Passifs : 7-8 | Promoteurs : 9-10
 
    conversation  = models.OneToOneField(
        Conversation,
        on_delete=models.CASCADE,
        related_name="evaluation",
    )
    client        = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="evaluations",
    )
    note_nps      = models.PositiveIntegerField(
        help_text="Note de 0 à 10 (NPS : 9-10=Promoteur, 7-8=Passif, 0-6=Détracteur)",
    )
    note_satisfaction = models.PositiveIntegerField(
        help_text="Note de 1 à 5 (satisfaction générale)",
    )
    commentaire   = models.TextField(blank=True)
    created_at    = models.DateTimeField(auto_now_add=True)
 
    def __str__(self):
        return f"Éval. Conv.#{self.conversation.id} — NPS:{self.note_nps}"
 
    class Meta:
        verbose_name = "Évaluation de conversation"
