# apps/credits/services.py
from decimal import Decimal
from datetime import date
from dateutil.relativedelta import relativedelta
 
def calculer_score_eligibilite(client, montant_demande, duree_mois):
    """Calcule un score d'éligibilité simplifié (0-100)."""
    # HYPOTHÈSE : algorithme simplifié pour le projet
    score = 50  # Score de base
 
    credits_precedents = client.demandes_credit.filter(statut="DECAISSEE")
    if credits_precedents.exists():
        retards = 0
        if retards == 0: score += 20
        elif retards <= 2: score += 10
 
    if not credits_precedents.exists() and montant_demande > 500000:
        score -= 10
 
    from django.utils import timezone
    if (timezone.now() - client.date_joined).days > 180:
        score += 10
 
    return max(0, min(100, score))
 
 
def generer_echeancier(demande):
    """Génère l'échéancier par amortissement constant."""
    from .models import EcheancierRemboursement
 
    montant      = demande.montant_approuve
    duree        = demande.duree_mois
    taux_mensuel = demande.taux_interet_annuel / 12 / 100
 
    if taux_mensuel > 0:
        mensualite = montant * (taux_mensuel * (1 + taux_mensuel)**duree)
        mensualite /= ((1 + taux_mensuel)**duree - 1)
    else:
        mensualite = montant / duree
 
    capital_restant = montant
    date_debut      = date.today()
    echeances       = []
 
    for i in range(1, duree + 1):
        date_echeance = date_debut + relativedelta(months=i)
        interet       = capital_restant * taux_mensuel
        capital       = mensualite - interet
        capital_restant -= capital
        echeances.append(EcheancierRemboursement(
            demande=demande, numero_echeance=i,
            date_echeance=date_echeance,
            montant_capital=round(capital, 2),
            montant_interet=round(interet, 2),
            montant_total=round(mensualite, 2),
        ))
 
    EcheancierRemboursement.objects.bulk_create(echeances)

# Matrice des transitions autorisées du workflow
# Format : {statut_actuel: [statuts_vers_lesquels_on_peut_aller]}
TRANSITIONS_AUTORISEES = {
    "SOUMISE":    ["EN_ANALYSE", "REJETEE"],
    "EN_ANALYSE": ["APPROUVEE", "REJETEE"],
    "APPROUVEE":  ["DECAISSEE", "REJETEE"],
    "DECAISSEE":  [],          # État terminal — plus de changement
    "REJETEE":    [],          # État terminal — plus de changement
}
 
 
def valider_transition(statut_actuel, nouveau_statut):
    """
    Vérifie que la transition de statut est autorisée.
    Lève une ValueError si la transition est interdite.
    """
    transitions = TRANSITIONS_AUTORISEES.get(statut_actuel, [])
    if nouveau_statut not in transitions:
        raise ValueError(
            f"Transition interdite : {statut_actuel} → {nouveau_statut}. "
            f"Transitions possibles : {transitions}"
        )
 
 
def changer_statut_avec_historique(demande, nouveau_statut, agent, commentaire=""):
    """
    Change le statut d'une demande ET enregistre l'historique.
    Valide la transition, met à jour les dates et génère une notification.
    """
    from django.utils import timezone
    from apps.notifications.models import Notification
    from .models import HistoriqueStatutCredit
 
    # 1. Valider la transition
    valider_transition(demande.statut, nouveau_statut)
 
    # 2. Enregistrer l'historique AVANT le changement
    HistoriqueStatutCredit.objects.create(
        demande          = demande,
        statut_precedent = demande.statut,
        nouveau_statut   = nouveau_statut,
        modifie_par      = agent,
        commentaire      = commentaire,
    )
 
    # 3. Mettre à jour les dates automatiquement
    demande.statut         = nouveau_statut
    demande.agent_traitant = agent
    if nouveau_statut == "APPROUVEE":
        demande.date_approbation  = timezone.now()
    if nouveau_statut == "DECAISSEE":
        demande.date_decaissement = timezone.now()
    if commentaire:
        demande.commentaire_agent = commentaire
    demande.save()
 
    # 4. Notification automatique au client
    Notification.objects.create(
        destinataire      = demande.client,
        type_notification = "CREDIT_STATUT",
        titre  = f"Votre demande de crédit #{demande.id} a été mise à jour",
        message= f"Nouveau statut : {demande.get_statut_display()}. {commentaire}",
        lien_reference = f"/credits/{demande.id}/",
    )
 
    # 5. Si approuvé : générer l'échéancier
    if nouveau_statut == "APPROUVEE" and demande.montant_approuve:
        generer_echeancier(demande)
 
    return demande
