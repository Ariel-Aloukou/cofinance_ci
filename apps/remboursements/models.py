from django.db import models
from django.conf import settings
from apps.credits.models import EcheancierRemboursement

# Create your models here.
class Paiement(models.Model):
    MOYEN_PAIEMENT_CHOICES = [
        ("ORANGE_MONEY", "Orange Money"), ("WAVE", "Wave"),
        ("MTN_MOMO", "MTN MoMo"),         ("ESPECES", "Espèces"),
    ]
    echeance = models.OneToOneField(
        EcheancierRemboursement,
        on_delete=models.CASCADE
    )

    agent = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="paiements_enregistres"
    )
    penalite_retard       = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    moyen_paiement        = models.CharField(max_length=15, choices=MOYEN_PAIEMENT_CHOICES)
    reference_transaction = models.CharField(max_length=100, blank=True)
    date_paiement         = models.DateTimeField(auto_now_add=True)
