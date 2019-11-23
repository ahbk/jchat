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
    gs = await consumer.group_enter(group)
    return gs

async def leave(consumer, group):
    """
    Unubscribe from messages in group and return list of current subscriptions
    """
    gs = await consumer.group_leave(group)
    return gs

async def messages(consumer, group, start=None, limit=None):
    """
    Retreive messages from group

    Parameter start is a message.pk and limit is the maximum number of messages
    to include forward (positive number) or backward (negative number) in time.

    Sensible default for start is last message and for limit -100.

    Example:
    start=42 and limit=0 => message 42 only
    start=42 and limit=10 => message 42 + the ten messages after 42
    start=42 and limit=-10 => message 42 + the ten messages before 42

    """
    def db():
        return [{
            'id': m.pk,
            'created': m.created.timestamp() * 1e3,
            'text': m.text,
            'sign': m.member.sign,
            'parents': [{'id': p.pk} for p in m.parents.all()]
            } for m in Message.objects.filter(member__group__sign=group)]
    ms = await database_sync_to_async(db)()

    return ms

async def post(consumer, group, text, parents=None):
    """
    Post a message in a group
    If group is not in session, use first message to create a member.
    """
    def db():
        try:
            member = Member.objects.get(
                    pk__in=my_members(consumer),
                    group__sign=group,
                    )
        except Member.DoesNotExist:
            g, created = Group.objects.get_or_create(sign=group)
            member = Member.objects.create(
                    sign=text,
                    group=g,
                    )
            my_members(consumer, add=member.pk)

        m = Message.objects.create(
                text=text,
                member=member,
                )

        if parents:
            m.parents.set(Message.objects.filter(pk__in=parents))

        return {
            'id': m.pk,
            'created': m.created.timestamp() * 1e3,
            'text': m.text,
            'sign': m.member.sign,
            'parents': [{'id': p.pk} for p in m.parents.all()]
            }
    m = await database_sync_to_async(db)()
    await consumer.group_send(group, m)

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
