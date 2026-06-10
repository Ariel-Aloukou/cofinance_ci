# apps/authentication/permissions.py — VERSION COMPLÈTE
 
from rest_framework import permissions
 
 
class EstClient(permissions.BasePermission):
    """Seuls les CLIENT peuvent accéder."""
    message = "Accès réservé aux clients."
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "CLIENT"
 
 
class EstAgent(permissions.BasePermission):
    """Les AGENT et ADMIN peuvent accéder."""
    message = "Accès réservé aux agents et administrateurs."
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ["AGENT", "ADMIN"]
 
 
class EstAdmin(permissions.BasePermission):
    """Seuls les ADMIN peuvent accéder."""
    message = "Accès réservé aux administrateurs."
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "ADMIN"
 
 
class EstProprietaire(permissions.BasePermission):
    """
    Le client ne peut accéder qu'à SES propres ressources.
    Les agents et admins ont accès à tout.
    """
    message = "Vous ne pouvez accéder qu'à vos propres données."
 
    def has_object_permission(self, request, view, obj):
        if request.user.role in ["AGENT", "ADMIN"]:
            return True
        # Vérifie que l'objet appartient au client connecté
        return getattr(obj, "client", getattr(obj, "user", None)) == request.user
 
 
class LectureSeulementSiClient(permissions.BasePermission):
    """
    Un client peut lire (GET) mais pas écrire (POST/PUT/PATCH/DELETE).
    Un agent/admin peut tout faire.
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.user.role in ["AGENT", "ADMIN"]:
            return True
        # Client : lecture seule
        return request.method in permissions.SAFE_METHODS
