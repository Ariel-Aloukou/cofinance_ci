# apps/remboursements/admin.py
from django.contrib import admin
from .models import Paiement

@admin.register(Paiement)
class PaiementAdmin(admin.ModelAdmin):
    list_display = ['id', 'echeance', 'agent', 'montant_paye',
                    'penalite_retard', 'moyen_paiement', 'date_paiement']
    list_filter  = ['moyen_paiement']