from .common import *
import os

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

DEBUG = False

ALLOWED_HOSTS = ['127.0.0.1', '172.20.10.2']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'blog-project',
        'USER': 'root',
        'PASSWORD': 'root',
    }
}
