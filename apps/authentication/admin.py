# apps/authentication/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, PresenceAgent


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    # Colonnes affichées dans la liste
    list_display  = ['username', 'email', 'first_name', 'last_name',
                     'role', 'region', 'telephone', 'is_active']
    list_filter   = ['role', 'region', 'is_active']
    search_fields = ['username', 'email', 'first_name', 'last_name', 'numero_cni']
    ordering      = ['role', 'last_name']

    # Ajouter les champs personnalisés dans le formulaire d'édition
    fieldsets = UserAdmin.fieldsets + (
        ('Informations COFINANCE CI', {
            'fields': ('role', 'telephone', 'region', 'adresse',
                       'date_naissance', 'numero_cni')
        }),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Informations COFINANCE CI', {
            'fields': ('role', 'telephone', 'region')
        }),
    )


@admin.register(PresenceAgent)
class PresenceAgentAdmin(admin.ModelAdmin):
    list_display = ['agent', 'statut', 'charge_courante',
                    'capacite_max', 'derniere_activite']
    list_filter  = ['statut']