from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.contrib.auth.models import User
from be.models import Message
from django.contrib.auth import authenticate
from channels import auth
from channels.db import database_sync_to_async
from django.db import IntegrityError

def groupname(*users):
    return ''.join(sorted(users))


class Chat(AsyncJsonWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def group_receive(self, event):
        await self.send_json(event['message'])

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
            return [ {'name': user.username } for user in User.objects.exclude(pk=self.scope['user'].pk) ]

        def messages(user):
            def fn():
                sent = Message.objects.filter(sender=self.scope['user'], receiver__username=user)
                received = Message.objects.filter(receiver=self.scope['user'], sender__username=user)
                return [ {
                    'text': message.text,
                    'timestamp': message.timestamp.timestamp() * 1e3,
                    'sender': message.sender.username,
                    'receiver': message.receiver.username,
                    } for message in (sent | received).order_by('pk') ]
            return fn

        def post(text, receiver):
            def fn():
                return Message.objects.create(
                        sender=self.scope['user'],
                        receiver=User.objects.get(username=receiver),
                        text=text,
                        )
            return fn

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

        if content['req'] == 'messages':
            content['res'] = False
            if self.scope['user'].is_authenticated:
                content['res'] = await database_sync_to_async(messages(content['receiver']))()
                
                if self.scope.get('last_group', False):
                    self.channel_layer.group_discard(self.scope['last_group'], self.channel_name)

                # Use sorted usernames to create a common group identifier with the receiver
                self.scope['last_group'] = group = groupname(content['receiver'], self.scope['user'].username)


                await self.channel_layer.group_add(group, self.channel_name)
            await self.send_json(content)

        if content['req'] == 'post':
            content['res'] = None
            if self.scope['user'].is_authenticated:
                message = await database_sync_to_async(post(content['text'], content['receiver']))()
                content['res'] = {
                        'text': message.text,
                        'timestamp': message.timestamp.timestamp() * 1e3,
                        'sender': message.sender.username,
                        'receiver': message.receiver.username,
                        'group': groupname(message.sender.username, message.receiver.username),
                        }

                await self.channel_layer.group_send(content['res']['group'], { 'type': 'group_receive', 'message': content })
