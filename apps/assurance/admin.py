# apps/assurance/admin.py
from django.contrib import admin
from .models import FormulaAssurance, Souscription

@admin.register(FormulaAssurance)
class FormulaAdmin(admin.ModelAdmin):
    list_display = ['nom', 'categorie', 'prime_mensuelle',
                    'capital_garanti', 'duree_mois', 'est_active']
    list_filter  = ['categorie', 'est_active']

@admin.register(Souscription)
class SouscriptionAdmin(admin.ModelAdmin):
    list_display = ['client', 'formule', 'statut',
                    'date_souscription', 'date_expiration']
    list_filter  = ['statut']