from .common import *
import os

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

DEBUG = False

ALLOWED_HOSTS = ['127.0.0.1', '172.20.10.2']
