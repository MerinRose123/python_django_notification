from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from notifier.consumers import NoseyConsumer

'''
application = ProtocolTypeRouter({
    "websocket": URLRouter([
        path("notifications/", NoseyConsumer),
    ])
})
'''
import chat.routing

application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': AuthMiddlewareStack(
        URLRouter(
            chat.routing.websocket_urlpatterns
        )
    ),
})

