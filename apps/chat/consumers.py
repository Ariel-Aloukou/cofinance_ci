import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Conversation, Message
 
class ChatConsumer(AsyncWebsocketConsumer):
    """Gère les connexions WebSocket. Chaque conversation = un groupe."""
 
    async def connect(self):
        self.conversation_id  = self.scope["url_route"]["kwargs"]["conversation_id"]
        self.room_group_name  = f"chat_{self.conversation_id}"
        conversation = await self.get_conversation(self.conversation_id)
        if not conversation:
            await self.close(); return
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()
        # Mettre l'agent en ligne automatiquement à la connexion WebSocket
        if self.scope["user"].role in ["AGENT", "ADMIN"]:
            await self.mettre_en_ligne(self.scope["user"])

        await self.send(text_data=json.dumps({"type": "connexion", "message": "Connecté"}))
 
    async def disconnect(self, close_code):
        async def disconnect(self, close_code):
            await self.channel_layer.group_discard(
            self.room_group_name, self.channel_name)
            # Mettre l'agent hors ligne à la déconnexion WebSocket
            if self.scope["user"].role in ["AGENT", "ADMIN"]:
                await self.mettre_hors_ligne(self.scope["user"])

        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
 
    async def receive(self, text_data):
        data         = json.loads(text_data)
        message_type = data.get("type", "message")
 
        if message_type == "message":
            contenu = data.get("contenu", "").strip()
            if not contenu: return
            message = await self.sauvegarder_message(
                self.conversation_id, self.scope["user"], contenu)
            await self.channel_layer.group_send(self.room_group_name, {
                "type": "chat.message",
                "message": {
                    "id": message.id,
                    "contenu": message.contenu,
                    "auteur_id": self.scope["user"].id,
                    "auteur_nom": self.scope["user"].get_full_name(),
                    "created_at": message.created_at.isoformat(),
                }
            })
 
        elif message_type == "frappe":  # Indicateur "en train d'écrire..."
            await self.channel_layer.group_send(self.room_group_name, {
                "type": "chat.frappe",
                "auteur_id":  self.scope["user"].id,
                "auteur_nom": self.scope["user"].get_full_name(),
            })
 
    async def chat_message(self, event):
        await self.send(text_data=json.dumps({"type": "message", "message": event["message"]}))
 
    async def chat_frappe(self, event):
        if event["auteur_id"] != self.scope["user"].id:
            await self.send(text_data=json.dumps({
                "type": "frappe", "auteur_nom": event["auteur_nom"]}))
 
    @database_sync_to_async
    def get_conversation(self, conv_id):
        try: return Conversation.objects.get(pk=conv_id)
        except Conversation.DoesNotExist: return None
 
    @database_sync_to_async
    def sauvegarder_message(self, conv_id, user, contenu):
        conv = Conversation.objects.get(pk=conv_id)
        if user.role in ["AGENT","ADMIN"] and conv.statut == "OUVERTE":
            conv.agent = user; conv.statut = "EN_COURS"; conv.save()
        return Message.objects.create(conversation=conv, auteur=user, contenu=contenu)
    
    @database_sync_to_async
    def mettre_en_ligne(self, user):
        from apps.authentication.models import PresenceAgent
        presence, _ = PresenceAgent.objects.get_or_create(agent=user)
        presence.statut = "DISPONIBLE"
        presence.save()
 
    @database_sync_to_async
    def mettre_hors_ligne(self, user):
        from apps.authentication.models import PresenceAgent
        try:
            presence = user.presence
            presence.statut = "HORS_LIGNE"
            presence.save()
        except PresenceAgent.DoesNotExist:
            pass

