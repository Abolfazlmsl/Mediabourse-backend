from django.conf.urls import url
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator, OriginValidator

from bourse.consumers import chartConsumer

application = ProtocolTypeRouter({
    'websocket': URLRouter([
        # url(r"^messages/(?P<username>[\w.@+-]+)/$", chartConsumer),
        url(r"^chart/$", chartConsumer),
    ])
    # 'websocket': AllowedHostsOriginValidator(
    #     AuthMiddlewareStack(
    #         URLRouter([
    #             url(r"^messages/(?P<username>[\w.@+-]+)/$", ChatConsumer),
    #         ])
    #     )
    # )
})