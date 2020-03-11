from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from channels import auth
from channels.db import database_sync_to_async
from django.db import IntegrityError


class Chat(AsyncJsonWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive_json(self, content):

        content['sid'] = self.scope['session'].session_key
        content['auth'] = self.scope['user'].is_authenticated

        def login():
            try:
                User.objects.create_user(content['name'], '', content['password'])
            except IntegrityError:
                pass

            user = authenticate(username=content['name'], password=content['password'])
            return user

        def users():
            return [ {'name': user.username } for user in User.objects.all() ]

        if content['req'] == 'login' and 'name' in content and 'password' in content:
            user = await database_sync_to_async(login)()

            if bool(user):
                await auth.login(self.scope, user)

            content['auth'] = content['res'] = bool(user)

            await self.send_json(content)

        if content['req'] == 'users':
            content['res'] = []
            if self.scope['user'].is_authenticated:
                content['res'] = await database_sync_to_async(users)()
            await self.send_json(content)

    async def group_receive(self, event):
        pass

    async def group_enter(self, group):
        pass

    async def group_leave(self, group):
        pass

    async def group_send(self, group, message):
        pass
