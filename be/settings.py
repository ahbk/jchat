# The important stuff
SECRET_KEY = 'c993#c%w_q%_z2yozc!ww7l(=uc0fmz-v%5d9h*xqinpm88-pm'
DEBUG = True
ALLOWED_HOSTS = ['*']

# Match no url (ROOT_URLCONF is required)
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
