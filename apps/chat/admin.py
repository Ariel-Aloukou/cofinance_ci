# apps/chat/admin.py
from django.contrib import admin
from .models import Conversation, Message, EvaluationConversation

@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ['id', 'client', 'agent', 'sujet', 'statut', 'created_at']
    list_filter  = ['statut']

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display  = ['id', 'conversation', 'auteur', 'contenu', 'created_at']
    search_fields = ['contenu', 'auteur__username']

admin.site.register(EvaluationConversation)