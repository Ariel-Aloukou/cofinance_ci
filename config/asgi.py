# config/asgi.py

import os
import django
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from apps.chat.routing import websocket_urlpatterns
from apps.chat.middleware import JWTAuthMiddleware  # ← nouveau

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": JWTAuthMiddleware(          # ← remplace AuthMiddlewareStack
        URLRouter(websocket_urlpatterns)
    ),
})