import os
from chat.consumers import ChatConsumer
import django
from channels.http import AsgiHandler
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from channels.auth import AuthMiddlewareStack

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

application = ProtocolTypeRouter({
  "http": AsgiHandler(),
  # Just HTTP for now. (We can add other protocols later.)
  'websocket': AuthMiddlewareStack(URLRouter([path('ws/chat/<slug:room_name>/', ChatConsumer.as_asgi())]))
})
