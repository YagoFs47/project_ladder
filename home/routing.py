from django.urls import path

from home import consumers

print("TO SENDO USADO")
websocket_urlpatterns = [
    path("ws", consumers.TestAsyncConsumer.as_asgi(), name="socket_app"),
]
