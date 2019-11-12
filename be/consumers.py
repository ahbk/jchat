from channels.generic.websocket import WebsocketConsumer
import json
from . import chat

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        try:
            msg = json.loads(text_data)
        except json.JSONDecodeError as e:
            msg = {
                    'result': None,
                    'error': "json couldn't decode '%s' (%s)" % (text_data, str(e)),
                    }
            self.send(text_data=json.dumps(msg))
            return

        try:
            fn = getattr(chat, msg['fn'])
        except TypeError as e:
            msg = {}
        except (KeyError, AttributeError) as e:
            msg['result'] = None
            msg['error'] = str(e)
            self.send(text_data=json.dumps(msg))
            return

        ctx = {
                'session': self.scope['session'],
                'groups': self.scope['session'].setdefault('groups', {}),
                'channel': self.channel_layer,
                }
        try:
            msg['result'] = fn(ctx, **msg.get('args', {}))
        except Exception as e:
            msg['result'] = None
            msg['error'] = str(e)
            self.send(text_data=json.dumps(msg))
            return


        self.send(text_data=json.dumps(msg))
