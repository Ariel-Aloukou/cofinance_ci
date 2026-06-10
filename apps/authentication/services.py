# apps/authentication/services.py

from .models import CustomUser, PresenceAgent


def obtenir_agents_disponibles():
    """
    Retourne la liste des agents actuellement disponibles.
    Utilisé par le système d'assignation automatique.
    """
    return PresenceAgent.objects.filter(
        statut="DISPONIBLE",
    ).select_related("agent")


def mettre_agent_en_ligne(user):
    """
    Passe le statut d'un agent à DISPONIBLE.
    Appelé à la connexion WebSocket.
    """
    presence, _ = PresenceAgent.objects.get_or_create(agent=user)
    presence.statut = "DISPONIBLE"
    presence.save()
    return presence


def mettre_agent_hors_ligne(user):
    """
    Passe le statut d'un agent à HORS_LIGNE.
    Appelé à la déconnexion WebSocket.
    """
    try:
        presence = user.presence
        presence.statut = "HORS_LIGNE"
        presence.save()
    except PresenceAgent.DoesNotExist:
        pass