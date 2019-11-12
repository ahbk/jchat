from asgiref.sync import async_to_sync
from django.utils.dateformat import format as dateformat
from .models import User, Group, Member, Message

"""
Command         Arguments       Description
sid             -               Obtain and print session id
memberships     -               List memberships associated to the session
new             sign            Start a new group
join            group, sign     Apply for membership in a group
detach          group           Remove membership from session
members         group           Show members in a group
enter           group           Subscribe to group
leave           group           Unsubscribe from group
messages        group           Retreive messages from group
echo            msg             Echo a message
post            group, msg      Send a message
"""
def sid(context):
    """
    Create a new session or load an existing and return session key.

    channels.sessions.SessionMiddlewareStack attempts to load a session on every request based on
    HTTP-header "Cookie: sessionid={sessionid}". If session_key is None, the client didn't pass
    the header or used an non-existing sessionid.

    Assume that the client has done its best setting header and create a new session for the
    client if none exist.
    """
    if context["session"].session_key is None:
        context['session'].create()

    return { 'sessionid': context['session'].session_key }

def new(context, sign):
    """
    Start a new group and join it with signature sign
    """
    g = Group.objects.create()
    m = Member.objects.create(sign=sign, group=g)

    context['groups'][g.pk] = m.pk
    context['session'].save()

    return { 'group': g.pk, 'sign': m.sign }

def memberships(context):
    ms = Member.objects.filter(pk__in=list(context['groups'].values()))

    return [{
        'group': {
            'id': m.group.pk,
            'created': m.group.created.timestamp() * 1e3,
            },
        'member': {
            'sign': m.sign,
            'created': m.created.timestamp() * 1e3,
            }
        } for m in ms]

def join(context, group, sign):
    g = Group.objects.get(pk=group)
    m = Member.objects.create(sign=sign, group=g)

    context['groups'][g.pk] = m.pk
    context['session'].save()

    return { 'group': g.pk, 'sign': m.sign }

def detach(context, group):
    member = context['groups'][group]
    del context['groups'][group]
    context['session'].save()
    return { 'group': group, 'member': member }

def messages(context, group):
    async_to_sync(context['channel'].group_add)('group', 'chat')
    ms = Message.objects.filter(member__group__pk=group)

    return [{
        'id': m.pk,
        'created': m.created.timestamp() * 1e3,
        'text': m.text,
        'sign': m.member.sign,
        'parents': [{'id': p.pk} for p in m.parents.all()]
        } for m in ms]

def post(context, text, group, parents):
    async_to_sync(context['channel'].group_send)(
            'group',
            {
                'type': 'chat_message',
                'message': text
                }
            )
    m = Message.objects.create(
            text=text,
            member=Member.objects.get(pk=context['groups'][group]),
            )

    if parents:
        m.parents.set(Message.objects.filter(pk__in=parents))

    return {
            'id': m.pk,
            'created': m.created.timestamp() * 1e3,
            }

def member(scope, group):
    return context['groups'].get(group, False)

def echo(context, message):
    print(message)
    return message

