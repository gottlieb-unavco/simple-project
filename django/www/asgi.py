"""
ASGI config for www project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os
from channels.http import AsgiHandler
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'www.settings')
django_asgi_app = get_asgi_application()

import kafka_test.channels.routing  # noqa


def create_app():
    return ProtocolTypeRouter({
        "http": AsgiHandler(),
        "websocket": AuthMiddlewareStack(
            URLRouter(
                kafka_test.channels.routing.websocket_urlpatterns
            )
        ),
    })

application = create_app()