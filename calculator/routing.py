from django.urls import re_path

from .consumers import CalculatorConsumer, TasksConsumer

websocket_urlpatterns = [
    re_path(r'ws/calculator/(?P<room>\w+)/$', CalculatorConsumer.as_asgi()),
    re_path(r'ws/tasks/', TasksConsumer.as_asgi())
]