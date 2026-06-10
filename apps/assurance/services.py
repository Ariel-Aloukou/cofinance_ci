from datetime import date, timedelta
from .models import Souscription
from apps.notifications.models import Notification
 
def verifier_expirations():
    """Notifie 15 jours avant l'expiration d'une souscription."""
    dans_15_jours = date.today() + timedelta(days=15)
    souscriptions = Souscription.objects.filter(
        statut="ACTIVE", date_expiration=dans_15_jours, notification_envoyee=False)
    for s in souscriptions:
        Notification.objects.create(
            destinataire=s.client, type_notification="ALERTE_ASSURANCE",
            titre="Votre assurance expire bientôt",
            message=f'La police "{s.formule.nom}" expire le {s.date_expiration.strftime("%d/%m/%Y")}.'
        )
        s.notification_envoyee = True
        s.save()
