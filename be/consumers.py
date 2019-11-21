import json
from channels.generic.websocket import AsyncWebsocketConsumer
from . import chat

class Chat(AsyncWebsocketConsumer):
    async def connect(self):
        self.current_groups = []
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        try:
            msg = json.loads(text_data)
        except json.JSONDecodeError as e:
            msg = {
                    'result': None,
                    'error': "json couldn't decode '%s' (%s)" % (text_data, str(e)),
                    }
            await self.send(text_data=json.dumps(msg))
            return

        try:
            chat.api[msg['fn']]
        except (KeyError) as e:
            msg['result'] = None
            msg['error'] = str(e)
            await self.send(text_data=json.dumps(msg))
            return

        try:
            msg['result'] = await getattr(chat, msg['fn'])(self, **msg.get('args', {}))
            if msg['result'] is None:
                return
        except Exception as e:
            msg['result'] = None
            msg['error'] = str(e)

        await self.send(text_data=json.dumps(msg))

    async def group_receive(self, event):
        await self.send(text_data=json.dumps(event))

    async def group_enter(self, group):
        await self.channel_layer.group_add(
            group,
            self.channel_name
        )
        self.current_groups.append(group)
        return self.current_groups

    async def group_leave(self, group):
        await self.channel_layer.group_discard(
            group,
            self.channel_name
        )
        self.current_groups.remove(group)
        return self.current_groups

    async def group_send(self, group, message):
        await self.channel_layer.group_send(
            group,
            {
                'type': 'group_receive',
                'message': message
            }
        )
