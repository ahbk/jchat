from channels.generic.websocket import AsyncJsonWebsocketConsumer
from . import chat

class Chat(AsyncJsonWebsocketConsumer):
    async def connect(self):
        ms = await chat.memberships(self)
        for m in ms:
            await self.group_enter(m['group']['sign'])
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive_json(self, content):
        message = await chat.route(self, content)
        await self.send_json(message)

    async def group_receive(self, event):
        await self.send_json(event['message'])

    async def group_enter(self, group):
        await self.channel_layer.group_add(
            group,
            self.channel_name
        )

    async def group_leave(self, group):
        await self.channel_layer.group_discard(
            group,
            self.channel_name
        )

    async def group_send(self, group, message):
        await self.channel_layer.group_send(
            group,
            {
                'type': 'group_receive',
                'message': message
            }
        )
