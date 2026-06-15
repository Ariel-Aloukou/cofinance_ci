from django.conf import settings
from django.db import models

# Create your models here.
class DemandeCredit(models.Model):
    STATUT_CHOICES = [  
        ("SOUMISE", "Soumise"),
        ("EN_ANALYSE", "En analyse"),
        ("APPROUVEE", "Approuvée"),
        ("DECAISSEE", "Décaissée"),
        ("REJETEE", "Rejetée"),
    ]
    PERIODICITE_CHOICES = [
        ("HEBDOMADAIRE", "Hebdomadaire"),
        ("BIHEBDOMADAIRE", "Bihebdomadaire"),
        ("MENSUEL", "Mensuel"),
    ]
    client = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="demandes_credit"
    )

    agent_traitant = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="credits_agent"
    )
    montant_demande   = models.DecimalField(max_digits=12, decimal_places=2)
    duree_mois        = models.PositiveIntegerField()
    periodicite       = models.CharField(max_length=15, choices=PERIODICITE_CHOICES)
    taux_interet_annuel = models.DecimalField(max_digits=5, decimal_places=2, default=18.00)
    objet_credit      = models.TextField()
    statut            = models.CharField(max_length=15, choices=STATUT_CHOICES)
    score_eligibilite = models.IntegerField(null=True, blank=True)
    montant_approuve  = models.DecimalField(max_digits=12, decimal_places=2, null=True)
    date_soumission   = models.DateTimeField(auto_now_add=True)
    date_approbation  = models.DateTimeField(null=True, blank=True)
    date_decaissement = models.DateTimeField(null=True, blank=True)
 
class EcheancierRemboursement(models.Model):
    demande = models.ForeignKey(
        DemandeCredit,
        on_delete=models.CASCADE,
        related_name="echeances"
    )
    numero_echeance   = models.PositiveIntegerField()
    date_echeance     = models.DateField()
    montant_capital   = models.DecimalField(max_digits=12, decimal_places=2)
    montant_interet   = models.DecimalField(max_digits=12, decimal_places=2)
    montant_total     = models.DecimalField(max_digits=12, decimal_places=2)
    est_paye          = models.BooleanField(default=False)

def chemin_piece(instance, filename):
    """Génère le chemin de stockage : credits/<client_id>/<demande_id>/<fichier>"""
    return f"credits/{instance.demande.client.id}/{instance.demande.id}/{filename}"
 
 
class PieceJustificative(models.Model):
    """
    Pièce justificative attachée à une demande de crédit.
    Stockée dans media/credits/<client_id>/<demande_id>/.
    """
    TYPE_CHOICES = [
        ("CNI",         "Carte Nationale d'Identité"),
        ("BULLETIN",    "Bulletin de salaire"),
        ("EXTRAIT_BANK","Relevé bancaire"),
        ("PHOTO",       "Photo d'identité"),
        ("AUTRE",       "Autre document"),
    ]
 
    demande       = models.ForeignKey(
        DemandeCredit,
        on_delete=models.CASCADE,
        related_name="pieces_justificatives_set",
    )
    type_document = models.CharField(max_length=15, choices=TYPE_CHOICES)
    fichier       = models.FileField(upload_to=chemin_piece)
    nom_original  = models.CharField(max_length=255, blank=True)
    taille_octets = models.PositiveIntegerField(default=0)
    uploaded_by   = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
    )
    created_at    = models.DateTimeField(auto_now_add=True)
 
    def save(self, *args, **kwargs):
        # Sauvegarde automatique du nom et de la taille
        if self.fichier:
            self.nom_original  = self.fichier.name
            self.taille_octets = self.fichier.size
        super().save(*args, **kwargs)
 
    def __str__(self):
        return f"{self.get_type_document_display()} — Crédit #{self.demande.id}"
 
    class Meta:
        verbose_name          = "Pièce justificative"
        verbose_name_plural   = "Pièces justificatives"

class HistoriqueStatutCredit(models.Model):
    """
    Trace chaque changement de statut d'une demande de crédit.
    Permet l'auditabilité complète du workflow.
    """
    demande          = models.ForeignKey(
        DemandeCredit,
        on_delete=models.CASCADE,
        related_name="historique_statuts",
    )
    statut_precedent = models.CharField(
        max_length=15,
        choices=DemandeCredit.STATUT_CHOICES,
        null=True, blank=True,
    )
    nouveau_statut   = models.CharField(
        max_length=15,
        choices=DemandeCredit.STATUT_CHOICES,
    )
    modifie_par      = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
    )
    commentaire      = models.TextField(blank=True)
    created_at       = models.DateTimeField(auto_now_add=True)
 
    def __str__(self):
        return f"Crédit #{self.demande.id} : {self.statut_precedent} → {self.nouveau_statut}"
 
    class Meta:
        verbose_name        = "Historique de statut"
        verbose_name_plural = "Historiques de statuts"
        ordering            = ["-created_at"]
