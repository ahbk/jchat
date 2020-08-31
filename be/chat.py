import sys
from channels.db import database_sync_to_async
from .models import User, Group, Member, Message

api = {
        'session': ((), "Obtain and print session id"),
        'memberships': ((), "List all memberships attached to session"),
        'join': (('group', 'member'), "Add membership to session"),
        'detach': (('group', 'member'), "Remove membership from session"),
        'members': (('group',), "List members in a group"),
        'enter': (('group',), "Subscribe to group"),
        'leave': (('group',), "Unsubscribe from group"),
        'messages': (('group', 'start', 'limit'), "Retreive messages from group"),
        'post': (('group', 'text', 'parents'), "Post a message"),
        'echo': (('group', 'text'), "Echo a text"),
        }

async def route(consumer, message):
    command = message['text'].split()
    text = 're: %s: %s.' % (message['text'], api[command[1]][1])
    payload = await getattr(sys.modules[__name__], command[1])(consumer, **message.get('payload', {}))
    
    return {
            'text': text,
            'parents': [ message['id'] ],
            'payload': payload,
            }

async def session(consumer):
    """
    Create a new session or load an existing and return session key.

    channels.sessions.SessionMiddlewareStack attempts to load a session on every request based on
    HTTP-header "Cookie: sessionid={sessionid}". If session_key isn't found, the client didn't pass
    the header or used an non-existing sessionid.

    Assume that the client has done its best setting header and create a new session for the
    client if none exist.
    """
    def db():
        if not consumer.scope["session"].exists(consumer.scope["session"].session_key):
            consumer.scope['session'].create()
        return {
            'id': consumer.scope['session'].session_key,
            'data': my_members(consumer),
            }
    session = await database_sync_to_async(db)()
    return session

async def memberships(consumer):
    def db():
        return [{
            'group': {
                'id': m.group.pk,
                'sign': m.group.sign,
                },
            'member': {
                'id': m.pk,
                'sign': m.sign,
                'created': m.created.timestamp() * 1e3,
                'notifications': m.notifications,
                }
            } for m in Member.objects.filter(pk__in=my_members(consumer))]
    memberships = await database_sync_to_async(db)()
    return memberships

async def join(consumer, group, member):
    """
    Join a group with a member and add to session
    """
    def db():
        g, created = Group.objects.get_or_create(sign=group)
        m = Member.objects.create(sign=member, group=g)

        my_members(consumer, add=m.pk)
    await database_sync_to_async(db)()

    ms = await consumer.memberships()
    return ms

async def detach(consumer, group, member):
    """
    Detach a group from session
    """
    def db():
        m = Member.objects.get(sign=member, group__sign=group)
        my_members(consumer, remove=m.pk)
    await database_sync_to_async(db)()

    ms = await consumer.memberships()
    return ms

async def members(consumer, group):
    """
    List all members of group
    """
    def db():
        return {m.sign: {
            'id': m.pk,
            'created': m.created.timestamp() * 1e3
            } for m in Group.objects.get(sign=group).member_set.all()}
    ms = await database_sync_to_async(db)()

    return ms

async def enter(consumer, group):
    """
    Subscribe to messages in group and return list of current subscriptions
    """
    await consumer.group_enter(group)

async def leave(consumer, group):
    """
    Unubscribe from messages in group and return list of current subscriptions
    """
    await consumer.group_leave(group)

async def messages(consumer, group=None):
    """
    Retreive messages from group
    """
    if group is None:
        ms = await memberships(consumer)
        groups = [ m['group']['sign'] for m in ms ]
    else:
        groups = [ group ]

    def db():
        return [{
            'pk': m.pk,
            'created': m.created.timestamp() * 1e3,
            'text': m.text,
            'sign': m.member.sign,
            'group': m.member.group.sign,
            'parents': [{'id': p.pk} for p in m.parents.all()]
            } for m in Message.objects.filter(member__group__sign__in=groups)]
    ms = await database_sync_to_async(db)()

    return ms

async def post(consumer, **message):
    """
    Post a message in a group
    If group is not in session, use first message to create a member.
    """
    def db():
        try:
            member = Member.objects.get(
                    pk__in=my_members(consumer),
                    group__sign=message['group'],
                    )
        except Member.DoesNotExist:
            g, created = Group.objects.get_or_create(sign=message['group'])
            member = Member.objects.create(
                    sign=message['text'],
                    group=g,
                    )
            my_members(consumer, add=member.pk)

        m = Message.objects.create(
                text=message['text'],
                member=member,
                )

        if message['parents']:
            m.parents.set(Message.objects.filter(pk__in=message['parents']))

        return {
            'pk': m.pk,
            'created': m.created.timestamp() * 1e3,
            'text': m.text,
            'group': m.member.group.sign,
            'sign': m.member.sign,
            'parents': [p.pk for p in m.parents.all()]
            }
    m = await database_sync_to_async(db)()
    await consumer.group_send(message['group'], m)

    return m

async def echo(consumer, group, text):
    message = {'text': text}
    await consumer.group_send(group, message)

def my_members(consumer, add=None, remove=None):
    consumer.scope['session'].setdefault('members', [])

    if not add is None:
        consumer.scope['session']['members'].append(add)

    if not remove is None:
        consumer.scope['session']['members'].remove(remove)

    consumer.scope['session'].save()
    return consumer.scope['session']['members']
