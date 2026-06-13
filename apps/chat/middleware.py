# apps/chat/middleware.py

from channels.middleware import BaseMiddleware
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth import get_user_model

User = get_user_model()


@database_sync_to_async
def get_user_from_token(token_key):
    """Récupère l'utilisateur depuis un token JWT."""
    try:
        token = AccessToken(token_key)
        user_id = token["user_id"]
        return User.objects.get(id=user_id)
    except Exception:
        return AnonymousUser()


class JWTAuthMiddleware(BaseMiddleware):
    """
    Middleware qui lit le token JWT depuis l'URL WebSocket.
    URL attendue : ws://localhost:8000/ws/chat/1/?token=VOTRE_TOKEN
    """
    async def __call__(self, scope, receive, send):
        # Lire le token depuis les query params
        from urllib.parse import parse_qs
        query_string = scope.get("query_string", b"").decode()
        params       = parse_qs(query_string)
        token_list   = params.get("token", [None])
        token_key    = token_list[0] if token_list else None

        if token_key:
            scope["user"] = await get_user_from_token(token_key)
        else:
            scope["user"] = AnonymousUser()

        return await super().__call__(scope, receive, send)