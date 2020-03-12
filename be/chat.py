from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from channels.db import database_sync_to_async
from django.db import IntegrityError
from be.models import Message

async def login(content):
    """
    Handle a login request
    """
    def db():
        try:
            User.objects.create_user(content['name'], '', content['password'])
        except IntegrityError:
            pass

        user = authenticate(username=content['name'], password=content['password'])
        return user

    if 'name' in content and 'password' in content:
        user = await database_sync_to_async(db)()
    else:
        user = None

    content['auth'] = bool(user)
    content['res'] = user

    return content

async def users(content):
    """
    Retreive a list of all users excluding current (logged in) user
    """
    def db():
        return [ {'name': user.username } for user in User.objects.exclude(pk=content['pk']) ]

    content['res'] = await database_sync_to_async(db)()
    return content

async def messages(content):
    """
    Retreive a list of messages between two users (regardless of who's sender and receiver)
    """
    sent = Message.objects.filter(sender__pk=content['pk'], receiver__username=content['receiver'])
    received = Message.objects.filter(receiver__pk=content['pk'], sender__username=content['receiver'])

    def db():
        return [ {
            'text': message.text,
            'timestamp': message.timestamp.timestamp() * 1e3,
            'sender': message.sender.username,
            'receiver': message.receiver.username,
            } for message in (sent | received).order_by('pk') ]

    content['res'] = await database_sync_to_async(db)()
    return content

async def post(content):
    """
    Store a message
    """
    def db():
        return Message.objects.create(
                sender=User.objects.get(pk=content['pk']),
                receiver=User.objects.get(username=content['receiver']),
                text=content['text'],
                )

    message = await database_sync_to_async(db)()

    content['res'] = {
            'text': message.text,
            'timestamp': message.timestamp.timestamp() * 1e3,
            'sender': message.sender.username,
            'receiver': message.receiver.username,
            'group': groupname(message.sender.username, message.receiver.username),
            }

    return content

def groupname(*users):
    """
    Create a distinct deterministic groupname based on two usernames
    """
    return ''.join(sorted(users))
