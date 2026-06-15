# apps/credits/admin.py
from django.contrib import admin
from .models import DemandeCredit, EcheancierRemboursement, HistoriqueStatutCredit, PieceJustificative

@admin.register(DemandeCredit)
class DemandeCreditAdmin(admin.ModelAdmin):
    list_display  = ['id', 'client', 'montant_demande', 'statut',
                     'score_eligibilite', 'agent_traitant', 'date_soumission']
    list_filter   = ['statut']
    search_fields = ['client__username', 'client__last_name']

@admin.register(EcheancierRemboursement)
class EcheancierAdmin(admin.ModelAdmin):
    list_display = ['demande', 'numero_echeance', 'date_echeance',
                    'montant_total', 'est_paye']
    list_filter  = ['est_paye']

admin.site.register(HistoriqueStatutCredit)
admin.site.register(PieceJustificative)