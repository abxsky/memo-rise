from .common import *

DEBUG = True

SECRET_KEY = 'django-insecure-4u&jpq)7c+d4*wt2t#jgt@ws)86btez2kh^yy!j!%o)cbqg^ky'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST':'localhost',
        'NAME': 'memorise_db',
        'USER': 'root',
        'PASSWORD': 'lij467'
    }
}
