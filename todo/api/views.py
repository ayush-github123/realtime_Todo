from todo.models import Task, Room
from todo.api.serializers import TaskSerializers, RoomSerializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializers
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Room.objects.filter(user=self.request.user)


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializers
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title', 'user']
    ordering_fields = ['created_at']

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    
    def perform_create(self, serializer):
        # Get room by name or create it
        room_name = self.request.data.get('room_name')
        room = Room.objects.get(name=room_name)

        # Save task and associate with the room
        serializer.save(user=self.request.user, room=room)


    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise PermissionDenied('You are not allowed to delete the task')
        instance.delete()