from django.db import models
from django.contrib.auth.models import User
# Create your models here.



class Room(models.Model):
    name = models.CharField(max_length=200, unique=True)
    user = models.ManyToManyField(User, related_name='rooms')

    def __str__(self):
        return self.name
    


class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=200)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='tasks')
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.title} - {self.room.name}"