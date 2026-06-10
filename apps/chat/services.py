# apps/chat/services.py

from apps.authentication.models import PresenceAgent
from django.db import models


def trouver_agent_disponible():
    """
    Retourne l'agent disponible avec la plus faible charge courante.
    Retourne None si aucun agent n'est disponible.
    """
    presence = PresenceAgent.objects.filter(
        statut="DISPONIBLE",
        charge_courante__lt=models.F("capacite_max"),
    ).order_by("charge_courante").select_related("agent").first()

    return presence.agent if presence else None


def assigner_agent_automatiquement(conversation):
    """
    Tente d'assigner automatiquement un agent disponible
    à une conversation nouvellement créée.
    """
    agent = trouver_agent_disponible()
    if agent:
        conversation.agent  = agent
        conversation.statut = "EN_COURS"
        conversation.save()
        # Incrémenter la charge de l'agent
        try:
            presence = agent.presence
            presence.charge_courante += 1
            presence.save()
        except PresenceAgent.DoesNotExist:
            pass
    return conversation


def liberer_agent(conversation):
    """
    Décrémente la charge de l'agent quand une conversation est fermée.
    """
    if conversation.agent:
        try:
            presence = conversation.agent.presence
            if presence.charge_courante > 0:
                presence.charge_courante -= 1
                presence.save()
        except PresenceAgent.DoesNotExist:
            pass


def calculer_nps():
    """
    Calcule le Net Promoter Score global.
    Formule : % Promoteurs (9-10) - % Détracteurs (0-6)
    Résultat entre -100 et +100. Objectif COFINANCE CI : 65 points.
    """
    from .models import EvaluationConversation

    total = EvaluationConversation.objects.count()
    if total == 0:
        return {
            "nps": 0,
            "total_reponses": 0,
            "message": "Aucune évaluation pour le moment.",
        }

    promoteurs  = EvaluationConversation.objects.filter(note_nps__gte=9).count()
    detracteurs = EvaluationConversation.objects.filter(note_nps__lte=6).count()
    nps         = round((promoteurs - detracteurs) / total * 100, 1)

    return {
        "nps":             nps,
        "total_reponses":  total,
        "promoteurs_pct":  round(promoteurs  / total * 100, 1),
        "detracteurs_pct": round(detracteurs / total * 100, 1),
        "objectif_nps":    65,
        "atteint":         nps >= 65,
    }