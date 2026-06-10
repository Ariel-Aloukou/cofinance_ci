from django.db import models
from django.conf import settings


class FormulaAssurance(models.Model):

    CATEGORIE_CHOICES = [
        ("VIE", "Assurance Vie"),
        ("SANTE", "Assurance Santé"),
        ("DECES", "Assurance Décès"),
        ("ACCIDENT", "Assurance Accident"),
    ]

    nom = models.CharField(max_length=100)
    categorie = models.CharField(max_length=20, choices=CATEGORIE_CHOICES)
    description = models.TextField()
    prime_mensuelle = models.DecimalField(max_digits=10, decimal_places=2)
    capital_garanti = models.DecimalField(max_digits=15, decimal_places=2)
    duree_mois = models.PositiveIntegerField()
    est_active = models.BooleanField(default=True)


class Souscription(models.Model):

    STATUT_CHOICES = [
        ("ACTIVE", "Active"),
        ("EXPIREE", "Expirée"),
        ("RESILIEE", "Résiliée"),
    ]

    client = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="souscriptions"
    )

    formule = models.ForeignKey(
        FormulaAssurance,
        on_delete=models.CASCADE,
        related_name="souscriptions"
    )

    statut = models.CharField(
        max_length=10,
        choices=STATUT_CHOICES
    )

    date_souscription = models.DateField(auto_now_add=True)
    date_expiration = models.DateField()
    notification_envoyee = models.BooleanField(default=False)