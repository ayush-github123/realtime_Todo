from rest_framework import serializers
from todo.models import Task, Room, User

class RoomSerializers(serializers.ModelSerializer):
    # user = serializers.StringRelatedField(many=True)  # Assuming this is ManyToMany

    class Meta:
        model = Room
        fields = ['id', 'name', 'user']


class TaskSerializers(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)  # Read-only, shows username
    room = serializers.PrimaryKeyRelatedField(queryset=Room.objects.all())  # Room field should be editable

    class Meta:
        model = Task
        fields = ['id', 'title', 'user', 'room', 'is_completed', 'created_at', 'updated_at']
