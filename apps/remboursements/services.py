from datetime import date, timedelta
from decimal import Decimal
 
def calculer_penalite_retard(echeance):
    """HYPOTHÈSE : 2% du montant impayé par semaine de retard."""
    if date.today() <= echeance.date_echeance:
        return Decimal("0.00")
    jours_retard   = (date.today() - echeance.date_echeance).days
    semaines_retard = max(1, jours_retard // 7)
    return round(echeance.montant_total * Decimal("0.02") * semaines_retard, 2)
 
def obtenir_alertes():
    """Retourne les échéances J-3 (à venir) et J+1 (en retard)."""
    from apps.credits.models import EcheancierRemboursement
    aujourd_hui = date.today()
    alertes_a_venir = EcheancierRemboursement.objects.filter(
        est_paye=False, date_echeance=aujourd_hui + timedelta(days=3))
    alertes_retard = EcheancierRemboursement.objects.filter(
        est_paye=False, date_echeance=aujourd_hui - timedelta(days=1))
    return alertes_a_venir, alertes_retard
