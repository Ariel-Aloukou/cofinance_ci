from django.contrib.auth.models import AbstractUser
from django.db import models
 
class CustomUser(AbstractUser):
    """Modèle utilisateur personnalisé avec trois rôles."""
    ROLE_CHOICES = [
        ("CLIENT", "Client"),
        ("AGENT", "Agent de terrain"),
        ("ADMIN", "Administrateur"),
    ]
    role          = models.CharField(max_length=10, choices=ROLE_CHOICES, default="CLIENT")
    telephone     = models.CharField(max_length=20, blank=True)
    region        = models.CharField(max_length=100, blank=True)
    adresse       = models.TextField(blank=True)
    date_naissance= models.DateField(null=True, blank=True)
    numero_cni    = models.CharField(max_length=50, blank=True, unique=True, null=True)
    created_at    = models.DateTimeField(auto_now_add=True)
    updated_at    = models.DateTimeField(auto_now=True)
 
    @property
    def est_client(self): return self.role == "CLIENT"
    @property
    def est_agent(self):  return self.role == "AGENT"
    @property
    def est_admin(self):  return self.role == "ADMIN"
 
    def __str__(self):
        return f"{self.get_full_name()} ({self.role})"
 
    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"


class PresenceAgent(models.Model):
    """
    Gère la présence en ligne et la disponibilité d'un agent.
    Mise à jour automatiquement par le WebSocket et manuellement via API.
    """
    STATUT_CHOICES = [
        ("DISPONIBLE",   "Disponible"),
        ("OCCUPE",       "Occupé"),
        ("ABSENT",       "Absent"),
        ("HORS_LIGNE",   "Hors ligne"),
    ]
 
    agent            = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="presence",
        limit_choices_to={"role__in": ["AGENT", "ADMIN"]},
    )
    statut           = models.CharField(
        max_length=12, choices=STATUT_CHOICES, default="HORS_LIGNE"
    )
    derniere_activite= models.DateTimeField(auto_now=True)
    charge_courante  = models.PositiveIntegerField(
        default=0,
        help_text="Nombre de conversations actives",
    )
    capacite_max     = models.PositiveIntegerField(
        default=5,
        help_text="Nombre maximum de conversations simultanées",
    )
 
    @property
    def est_disponible(self):
        return (
            self.statut == "DISPONIBLE"
            and self.charge_courante < self.capacite_max
        )
 
    def __str__(self):
        return f"{self.agent.get_full_name()} — {self.statut}"
 
    class Meta:
        verbose_name = "Présence agent"
        verbose_name_plural = "Présences agents"