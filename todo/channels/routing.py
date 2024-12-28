from django.urls import path
from todo.channels.consumers import TaskConsumer

websocket_urlpatterns = [
    path('ws/tasks/<str:room_name>/', TaskConsumer.as_asgi())
]