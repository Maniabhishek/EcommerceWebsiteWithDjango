from .base import *

DEBUG = False

ALLOWED_HOSTS = ['IP-ADDRESS','WWW.MY-WEBSITE.COM']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME':'your database',
        'USER':'your db user name',
        'PASSWORD':'YOUR DB PASSWORD',
        'HOST': 'LOCALHOST',
        'PORT':'',
    }
}

