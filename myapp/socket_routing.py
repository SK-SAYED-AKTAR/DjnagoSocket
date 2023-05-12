from django.urls import path
from . import consumer

ws_urlpatterns = [
    path("ws/sc", consumer.SayedAsyncConsumer.as_asgi())
]