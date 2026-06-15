from django.shortcuts import render
from .serializers import NotificationSerializer
from .models import Notification

# Create your views here.
from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
 
class NotificationListView(generics.ListAPIView):
    serializer_class   = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Cette ligne est OBLIGATOIRE — filtre par utilisateur connecté
        return Notification.objects.filter(
            destinataire=self.request.user
        ).order_by('-created_at')
 
class MarquerLuView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def patch(self, request, pk):
        notif = Notification.objects.get(pk=pk, destinataire=request.user)
        notif.est_lu = True; notif.save()
        return Response({"status": "ok"})
 
class ToutMarquerLuView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def patch(self, request):
        Notification.objects.filter(destinataire=request.user, est_lu=False).update(est_lu=True)
        return Response({"status": "toutes lues"})
