ROOT_URLCONF = __name__
urlpatterns = []

# The application
INSTALLED_APPS = [ 'channels', 'be' , 'django.contrib.sessions']

ASGI_APPLICATION = 'be.routing.application'
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('127.0.0.1', 6379)],
        },
    },
}


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'be/db.sqlite3',
    }
}
