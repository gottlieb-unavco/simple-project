# chat/routing.py
from django.urls import re_path

from kafka_test.channels import consumers

websocket_urlpatterns = [
    re_path(r'ws/example/$', consumers.ExampleConsumer.as_asgi()),
]
