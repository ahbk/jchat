from channels.routing import ProtocolTypeRouter, URLRouter
from channels.sessions import SessionMiddlewareStack
from django.urls import path
from . import consumers

application = ProtocolTypeRouter({
    'websocket': SessionMiddlewareStack(URLRouter([
        path('chat/', consumers.ChatConsumer),
        ]))
    })
