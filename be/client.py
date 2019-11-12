import urwid
import asyncio
import os
import websockets
import json
import logging
from aiofile import AIOFile, Reader, Writer

logging.basicConfig(filename=os.path.abspath(__file__) + '.log', level=logging.DEBUG)

class History(list):
    def __init__(self):
        self.pointer = 0
        self.append('')

    def add(self, item):
        self[len(self) - 1] = item
        self.append('')
        self.pointer = len(self) - 1

    def prev(self):
        self.pointer = max(self.pointer - 1, 0)
        return self[self.pointer]

    def next(self):
        self.pointer = min(self.pointer + 1, len(self) - 1)
        return self[self.pointer]

    def last(self):
        self.pointer = len(self) - 1
        return self[self.pointer]

class Input(urwid.Edit):
    def keypress(self, size, key):
        if key == 'esc':
            edit.edit_text = history.last()

        if key == 'up':
            history[history.pointer] = edit.edit_text
            edit.edit_text = history.prev()

        if key == 'down':
            history[history.pointer] = edit.edit_text
            edit.edit_text = history.next()

        if key == 'enter':
            history.add(edit.edit_text)
            feed.set_text(feed.text + '\n< ' + edit.edit_text)
            send(edit.edit_text)
            edit.edit_text = ''

        if key not in('up', 'down', 'enter'):
            return super(Input, self).keypress(size, key)

def parse(fn, args):
    commands = {
                'sid': ((), "Obtain and print session id"),
                'memberships': ((), "List memberships associated to the session"),
                'new': (('sign',), "Start a new group and join it with signature sign"),
                'join': (('group', 'sign'), "Apply for membership in a group"),
                'detach': (('group',), "Remove membership from session"),
                'members': (('group',), "Show members in a group"),
                'enter': (('group',), "Subscribe to group"),
                'leave': (('group',), "Unsubscribe from group"),
                'messages': (('group',), "Retreive messages from group"),
                'echo': (('group', 'text'), "Echo a message"),
                'post': (('group', 'text'), "Send a message"),
                'help': (('command',), "Display help text for commands"),
                }
    try:
        keys, description = commands[fn]
    except KeyError:
        write(f"'{fn}' is not a valid command")
        return None

    if not len(keys) == len(args):
        write(f"{fn} takes exactly {len(keys)} arguments, ':{fn} {' '.join(keys)}'.")
        return None

    if fn == 'help':
        try:
            keys, description = commands[args[0]]
        except KeyError:
            write(f"'{args[0]}' is not a valid command")
            return None

        write(f"{description}: ':{args[0]} {' '.join(keys)}'.")
        return None

    return json.dumps({'fn': fn, 'args': dict(zip(keys, args))})

def write(message):
    feed.set_text(feed.text + '\n> ' + str(message))

def send(message):
    if message[0] == ':':
        c = message[1:].split(' ')
        message = parse(c[0], c[1:])

    if message:
        outbox.put_nowait(message)

async def main():
    sid = await read_sessionid()
    async with websockets.connect(uri, extra_headers=[('Cookie', f'sessionid={sid}')]) as websocket:
        await handler(websocket, '')

async def handler(websocket, path):
    consumer_task = asyncio.ensure_future(
        consumer_handler(websocket, path))
    producer_task = asyncio.ensure_future(
        producer_handler(websocket, path))
    done, pending = await asyncio.wait(
        [consumer_task, producer_task],
        return_when=asyncio.FIRST_COMPLETED,
    )
    for task in pending:
        task.cancel()

async def consumer_handler(websocket, path):
    async for message in websocket:
        await consumer(message)

async def producer_handler(websocket, path):
    while True:
        message = await outbox.get()
        await websocket.send(message)
        
async def write_sessionid(sid):
    async with AIOFile(os.path.join(cwd, 'sessionid'), 'w+') as afp:
        await afp.write(sid)
        sid = await afp.read()
        return sid

async def read_sessionid():
    async with AIOFile(os.path.join(cwd, 'sessionid'), 'r') as afp:
        sid = await afp.read()
        return sid

async def consumer(text_data):
    data = json.loads(text_data)
    message = text_data

    if data.get('type') == 'group_receive':
        write(data)
    elif data.get('result', None) is None:
        write(f"Failed: {data['error']}")
    elif data['fn'] == 'sid':
        sid = await write_sessionid(data['result']['sessionid'])
        write(f"Your sessionid: {sid}")
    elif data['fn'] in ('memberships', 'join', 'detach'):
        ms = [f"{m['member']['sign']}@{m['group']['id']}" for m in data['result']]
        write("Current memberships: " + ', '.join(ms))
    elif data['fn'] == 'new':
        write(f"Created new group: {data['result']['sign']}@{data['result']['group']}")
    elif data['fn'] == 'members':
        ms = [m['sign'] for m in data['result']]
        write(f"Members of group {data['args']['group']}: " + ', '.join(ms))
    else:
        feed.set_text(feed.text + '\n> ' + message)

loop = asyncio.get_event_loop()

uri = 'ws://localhost:8000/chat/'
cwd = os.path.dirname(os.path.abspath(__file__))
outbox = asyncio.Queue()
history = History()

feed = urwid.Text('- - -')
div = urwid.Divider()
edit = Input('Message: ')
pile = urwid.Pile([feed, div, edit])
fill = urwid.Filler(pile, valign='bottom')

urwid_loop = urwid.MainLoop(
        fill,
        event_loop=urwid.AsyncioEventLoop(loop=loop),
        )

loop.create_task(main())

urwid_loop.start()
try:
    loop.run_forever()
except BaseException:
    urwid_loop.stop()
