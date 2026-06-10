from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Count, Sum, Q, Avg
from django.utils import timezone
from django.utils.dateparse import parse_date
from datetime import timedelta
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from apps.authentication.permissions import EstAdmin
from apps.credits.models import DemandeCredit, EcheancierRemboursement
from apps.assurance.models import Souscription
from apps.chat.models import Conversation
 
 
@extend_schema(
    tags=["Dashboard"],
    summary="Indicateurs clés avec filtres date / agent / région",
    parameters=[
        OpenApiParameter("date_debut", OpenApiTypes.DATE,
                         description="Date de début (YYYY-MM-DD)"),
        OpenApiParameter("date_fin",   OpenApiTypes.DATE,
                         description="Date de fin (YYYY-MM-DD)"),
        OpenApiParameter("agent_id",   OpenApiTypes.INT,
                         description="Filtrer par ID d'agent"),
        OpenApiParameter("region",     OpenApiTypes.STR,
                         description="Filtrer par région (ex: Yopougon)"),
    ]
)
class StatsGlobalesView(APIView):
    permission_classes = [EstAdmin]
 
    def get(self, request):
        # ─── Lecture des filtres ──────────────────────────────────
        date_debut = parse_date(request.query_params.get("date_debut", "")) \
                     or (timezone.now() - timedelta(days=30)).date()
        date_fin   = parse_date(request.query_params.get("date_fin", "")) \
                     or timezone.now().date()
        agent_id   = request.query_params.get("agent_id")
        region     = request.query_params.get("region")
 
        # ─── Filtres de base ─────────────────────────────────────
        filtre_credits = Q(date_soumission__date__range=[date_debut, date_fin])
        if agent_id:
            filtre_credits &= Q(agent_traitant__id=agent_id)
        if region:
            filtre_credits &= Q(client__region__icontains=region)
 
        # ─── Volume de crédits par statut ────────────────────────
        credits_qs = DemandeCredit.objects.filter(filtre_credits)
        credits_par_statut = dict(
            credits_qs.values_list("statut")
            .annotate(n=Count("id")).values_list("statut", "n")
        )
 
        # ─── Montant total décaissé sur la période ───────────────
        montant_total_decaisse = credits_qs.filter(
            statut="DECAISSEE"
        ).aggregate(total=Sum("montant_approuve"))["total"] or 0
 
        # ─── Taux de recouvrement sur la période ────────────────
        echeances = EcheancierRemboursement.objects.filter(
            date_echeance__range=[date_debut, date_fin]
        )
        if agent_id:
            echeances = echeances.filter(demande__agent_traitant__id=agent_id)
        if region:
            echeances = echeances.filter(demande__client__region__icontains=region)
        total_ech  = echeances.count()
        payees_ech = echeances.filter(est_paye=True).count()
        taux_recouvrement = round(payees_ech / total_ech * 100, 2) if total_ech else 0
 
        # ─── Souscriptions actives ───────────────────────────────
        filtre_assurance = Q(statut="ACTIVE")
        if region:
            filtre_assurance &= Q(client__region__icontains=region)
        souscriptions_actives = Souscription.objects.filter(filtre_assurance).count()
 
        # ─── Conversations support ouvertes ─────────────────────
        conversations_ouvertes = Conversation.objects.filter(
            statut__in=["OUVERTE", "EN_COURS"]
        ).count()
 
        # ─── Conversations NON TRAITÉES (ouvertes > 1h sans réponse)
        seuil_non_traite = timezone.now() - timedelta(hours=1)
        conversations_non_traitees = Conversation.objects.filter(
            statut="OUVERTE",
            agent__isnull=True,
            created_at__lt=seuil_non_traite,
        ).count()
 
        return Response({
            "filtres_appliques": {
                "date_debut": str(date_debut),
                "date_fin":   str(date_fin),
                "agent_id":   agent_id,
                "region":     region,
            },
            "credits_par_statut":          credits_par_statut,
            "montant_total_decaisse_fcfa":  float(montant_total_decaisse),
            "taux_recouvrement_pct":        taux_recouvrement,
            "souscriptions_actives":        souscriptions_actives,
            "conversations_ouvertes":       conversations_ouvertes,
            "conversations_non_traitees":   conversations_non_traitees,
            "date_calcul":                  timezone.now().isoformat(),
        })

@extend_schema(
    tags=["Dashboard"],
    summary="Liste des conversations en attente d'agent",
)
class ConversationsNonTraiteesView(APIView):
    permission_classes = [EstAdmin]
 
    def get(self, request):
        """
        Retourne les conversations :
        - Sans agent assigné
        - Statut OUVERTE
        - Triées par date (les plus anciennes en premier)
        """
        from apps.chat.models import Conversation
        from apps.chat.serializers import ConversationSerializer
 
        conversations = Conversation.objects.filter(
            statut="OUVERTE",
            agent__isnull=True,
        ).order_by("created_at").select_related("client")
 
        data = []
        for conv in conversations:
            attente_minutes = int(
                (timezone.now() - conv.created_at).total_seconds() / 60
            )
            data.append({
                "id":               conv.id,
                "client_nom":       conv.client.get_full_name(),
                "client_region":    conv.client.region,
                "sujet":            conv.sujet,
                "attente_minutes":  attente_minutes,
                "created_at":       conv.created_at.isoformat(),
            })
 
        return Response({
            "total":         len(data),
            "conversations": data,
        })
