from .common import *

SECRET_KEY = 'g-)4nx^l)mv=@du%j#5pi9!%-r^9b@5lcg3=&**8us*2aap59_'

DEBUG = True

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR.parent / 'blog-project.db',
    }
}

