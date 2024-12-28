from django.urls import path, include
from rest_framework.routers import DefaultRouter
from todo.api.views import TaskViewSet, RoomViewSet

router = DefaultRouter()
router.register('tasks', TaskViewSet, basename='task')
router.register('rooms', RoomViewSet, basename='room')


urlpatterns = [
    path('', include(router.urls)),
]

