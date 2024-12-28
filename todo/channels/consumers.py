from channels.generic.websocket import AsyncWebsocketConsumer
import json
from asgiref.sync import sync_to_async
from channels.exceptions import DenyConnection

class TaskConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        from todo.models import Room, Task

        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room, created = await sync_to_async(Room.objects.get_or_create)(name=self.room_name)
        self.group_name = f"room_{self.room_name}"


        await sync_to_async(self.room.user.add)(self.scope['user'])

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        past_tasks = await sync_to_async(list)(Task.objects.filter(room=self.room).order_by('-created_at'))

        await self.accept()

        if past_tasks:
            for task in past_tasks:
                username = await sync_to_async(lambda: task.user.username)()
                await self.send(text_data=json.dumps({
                    'message': task.title,
                    'username': username,
                }))


    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )




    async def receive(self, text_data):
        from todo.models import Room, Task
        data = json.loads(text_data)  # convert text_data to json format
        message = data.get('message', "")
        action = data.get('action', "")
        username = self.scope['user'].username if self.scope['user'].is_authenticated else DenyConnection

        if  action == 'add_task':
            
            await sync_to_async(Task.objects.create)(
                room=self.room,
                user=self.scope['user'],
                title=message,
            )

            await self.channel_layer.group_send(
                self.group_name,
                {
                    'type': 'task_update',
                    'username': username,
                    'message': message,
                }
            )

    async def task_update(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'username': event['username'],
        }))
