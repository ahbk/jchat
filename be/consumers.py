from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels import auth
from . import chat

class Chat(AsyncJsonWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def group_receive(self, event):
        await self.send_json(event['message'])

    async def receive_json(self, content):

        # Add session id and auth flag to every response
        content['sid'] = self.scope['session'].session_key
        content['auth'] = self.scope['user'].is_authenticated

        if content['req'] == 'login':
            content = await chat.login(content)

            if bool(content['res']):
                await auth.login(self.scope, content['res'])

            content['res'] = bool(content['res'])
            await self.send_json(content)

            return

        # The request handlers below are for authenticated users only
        if not self.scope['user'].is_authenticated:
            await self.send_json(content)
            return

        content['pk'] = self.scope['user'].pk

        # Get a list of all users
        if content['req'] == 'users':
            await self.send_json(await chat.users(content))

        # Get a list of all messages with a selected user
        if content['req'] == 'messages':
            await self.send_json(await chat.messages(content))

            # If we're added to a group, leave it. We only want to subscribe to selected user.
            if self.scope.get('last_group', False):
                self.channel_layer.group_discard(self.scope['last_group'], self.channel_name)

            # Use sorted usernames to create a common group identifier with the receiver
            self.scope['last_group'] = group = chat.groupname(content['receiver'], self.scope['user'].username)
            await self.channel_layer.group_add(group, self.channel_name)

        # Post a message
        if content['req'] == 'post':
            content = await chat.post(content)
            await self.channel_layer.group_send(content['res']['group'], { 'type': 'group_receive', 'message': content })
