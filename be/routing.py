from channels.routing import ProtocolTypeRouter, URLRouter
from channels.sessions import SessionMiddlewareStack
from django.urls import path
from .consumers import Chat

application = ProtocolTypeRouter({
    'websocket': SessionMiddlewareStack(URLRouter([
        path('', Chat),
        ]))
    })
