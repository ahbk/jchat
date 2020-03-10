INSTALLED_APPS = [
        'channels',
        'be', # so makemigrations pick up models.py
        'django.contrib.sessions',
        'django.contrib.auth', 'django.contrib.contenttypes', # auth needs contenttypes
        ]

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

ROOT_URLCONF = __name__ # Make this module ROOT_URLCONF...
urlpatterns = [] # ..and noop built-in routing (channel routes are located in routing.py)

