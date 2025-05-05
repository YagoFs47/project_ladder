import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

import home.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ladder_server.settings')


application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": AuthMiddlewareStack(
            URLRouter(
                home.routing.websocket_urlpatterns
            )
        )
    }
)
