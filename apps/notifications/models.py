from django.db import models
from django.conf import settings

# Create your models here.
class Notification(models.Model):
    TYPE_CHOICES = [
        ("CREDIT_STATUT", "Changement de statut crédit"),
        ("REMBOURSEMENT", "Remboursement enregistré"),
        ("ASSURANCE", "Souscription confirmée"),
        ("ALERTE_ECHEANCE", "Alerte échéance"),
        ("ALERTE_ASSURANCE", "Alerte expiration assurance"),
    ]
    destinataire       = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name="notifications")
    type_notification  = models.CharField(max_length=25, choices=TYPE_CHOICES)
    titre              = models.CharField(max_length=200)
    message            = models.TextField()
    est_lu             = models.BooleanField(default=False)
    lien_reference     = models.CharField(max_length=200, blank=True)
    created_at         = models.DateTimeField(auto_now_add=True)
