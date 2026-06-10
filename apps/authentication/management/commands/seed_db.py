# apps/authentication/management/commands/seed_db.py

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.credits.models import DemandeCredit
from apps.assurance.models import FormulaAssurance
from apps.chat.models import Conversation, EvaluationConversation, Message
from apps.authentication.models import PresenceAgent
from apps.chat.models import Conversation
from apps.credits.models import HistoriqueStatutCredit


User = get_user_model()


class Command(BaseCommand):
    help = 'Charge les données de démonstration pour COFINANCE CI'

    def handle(self, *args, **kwargs):
        self.stdout.write('Chargement des données...')

        # ── Administrateur ─────────────────────────────────────
        admin, created = User.objects.get_or_create(
            username='admin_cofinance',
            defaults={
                'email':        'admin@cofinance.ci',
                'first_name':   'Directeur',
                'last_name':    'COFINANCE',
                'role':         'ADMIN',
                'region':       'Abidjan-Plateau',
                'is_staff':     True,
                'is_superuser': True,
            }
        )
        if created:
            admin.set_password('Admin@2026')
            admin.save()
            self.stdout.write('  ✅ Admin créé')

        # ── Agent de terrain ───────────────────────────────────
        agent, created = User.objects.get_or_create(
            username='agent_kouassi',
            defaults={
                'email':      'kouassi@cofinance.ci',
                'first_name': 'Kouassi',
                'last_name':  'AHOUSSI',
                'role':       'AGENT',
                'region':     'Yopougon',
                'telephone':  '+225 07 12 34 56',
            }
        )
        if created:
            agent.set_password('Agent@2026')
            agent.save()
            self.stdout.write('  ✅ Agent créé')

        # ── Client ─────────────────────────────────────────────
        client, created = User.objects.get_or_create(
            username='aya_kone',
            defaults={
                'email':       'aya.kone@gmail.com',
                'first_name':  'Aya',
                'last_name':   'KONÉ',
                'role':        'CLIENT',
                'region':      'Abobo',
                'telephone':   '+225 05 98 76 54',
                'numero_cni':  'CI-0123456789',
            }
        )
        if created:
            client.set_password('Client@2026')
            client.save()
            self.stdout.write('  ✅ Client créé')

        # ── Présence de l'agent ────────────────────────────────
        PresenceAgent.objects.get_or_create(
            agent=agent,
            defaults={"statut": "DISPONIBLE", "charge_courante": 1, "capacite_max": 5}
        )


        # ── Formule d'assurance ────────────────────────────────
        formule, _ = FormulaAssurance.objects.get_or_create(
            nom='Assurance Vie Essentielle',
            defaults={
                'categorie':       'VIE',
                'description':     'Protection vie adaptée aux micro-entrepreneurs',
                'prime_mensuelle': 2500,
                'capital_garanti': 1500000,
                'duree_mois':      12,
            }
        )
        self.stdout.write('  ✅ Formule assurance créée')

        # ── Demande de crédit ──────────────────────────────────
        if not DemandeCredit.objects.filter(client=client).exists():
            demande = DemandeCredit.objects.create(
                client=client,
                agent_traitant=agent,
                montant_demande=250000,
                duree_mois=6,
                periodicite='MENSUEL',
                taux_interet_annuel=18.00,
                objet_credit='Achat de stock pour commerce de tissu',
                statut='EN_ANALYSE',
                score_eligibilite=72,
            )
            self.stdout.write('  ✅ Demande de crédit créée')

           # Créer un historique de statut pour la demande existante
            demande = DemandeCredit.objects.filter(client=client).first()
            if demande and not demande.historique_statuts.exists():
                HistoriqueStatutCredit.objects.create(
                demande          = demande,
                statut_precedent = "SOUMISE",
                nouveau_statut   = "EN_ANALYSE",
                modifie_par      = agent,
                commentaire      = "Dossier reçu et pris en charge.",
            )


        # ── Conversation de chat ───────────────────────────────
        if not Conversation.objects.filter(client=client).exists():
            conv = Conversation.objects.create(
                client=client,
                agent=agent,
                sujet='Question sur ma demande de crédit',
                statut='EN_COURS',
            )
            Message.objects.create(
                conversation=conv,
                auteur=client,
                contenu='Bonjour, quand est-ce que mon dossier sera traité ?',
            )
            Message.objects.create(
                conversation=conv,
                auteur=agent,
                contenu='Bonjour Aya, votre dossier est en cours d\'analyse. Réponse sous 48h.',
            )
            self.stdout.write('  ✅ Conversation de chat créée')
            
        conv_fermee = Conversation.objects.filter(statut="FERMEE").first()
        if conv_fermee and not hasattr(conv_fermee, "evaluation"):
            EvaluationConversation.objects.create(
                conversation      = conv_fermee,
                client            = client,
                note_nps          = 9,
                note_satisfaction = 5,
                commentaire       = "Très bon service, agent réactif !",
            )
 
        self.stdout.write('  PresenceAgent → agent_kouassi : DISPONIBLE')


        # ── Résumé final ───────────────────────────────────────
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('✅ Données de démonstration chargées !'))
        self.stdout.write('')
        self.stdout.write('Comptes disponibles :')
        self.stdout.write('  Admin  → username: admin_cofinance | password: Admin@2026')
        self.stdout.write('  Agent  → username: agent_kouassi   | password: Agent@2026')
        self.stdout.write('  Client → username: aya_kone        | password: Client@2026')
        self.stdout.write('')
        self.stdout.write('Interface admin    : http://127.0.0.1:8000/admin/')
        self.stdout.write('Documentation API  : http://127.0.0.1:8000/api/docs/')