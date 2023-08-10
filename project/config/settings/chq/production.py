from config.settings.base import *

SECRET_KEY = '&7lhj(&jl8ijq*dg(^&!vy-omxp^sea9de6p=@%qx-ugw=s%!o'

DEBUG = False 

ALLOWED_HOSTS = [
    '0.0.0.0',
    'localhost',
    '.takenexams.com',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'd50abcvmcdthnj',
        'USER': 'egywzjfmrwhmll',
        'PASSWORD': 'e43dd9c0853a2257f2ec5d5f05fcc1b4b8857865b7d84ea03d1eb54ccdebbf2d',
        'HOST': 'ec2-79-125-6-250.eu-west-1.compute.amazonaws.com',
        'PORT': '5432',
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.eu.mailgun.org'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'postmaster@mg.takenexams.com'
EMAIL_HOST_PASSWORD = 'e0084ba8a0bade1d1f434b8c0cc53f05-52b0ea77-e5d05ae5'


STATIC_URL = 'https://cdn.takenexams.com/chq.takenexams.com/'

WEBDAV_URL = 'https://prod_takenexams@takenexams.com:sw26t2LVWYjZ@webdisk.takenexams.com/'
WEBDAV_PUBLIC_URL = STATIC_URL + 'img/content/'

DEFAULT_FILE_STORAGE = 'django_webdav_storage.storage.WebDavStorage'

