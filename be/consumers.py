from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from channels.db import database_sync_to_async
from django.db import IntegrityError


class Chat(AsyncJsonWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive_json(self, content):
        def login():
            try:
                User.objects.create_user(content['name'], '', content['password'])
            except IntegrityError:
                pass

            return authenticate(username=content['name'], password=content['password'])

        if content['req'] == 'login' and 'name' in content and 'password' in content:
            content['res'] = bool(await database_sync_to_async(login)())
            await self.send_json(content)

    async def group_receive(self, event):
        pass

    async def group_enter(self, group):
        pass

    async def group_leave(self, group):
        pass

    async def group_send(self, group, message):
        pass
