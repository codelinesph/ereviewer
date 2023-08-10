from config.settings.base import *

SECRET_KEY = '&7lhj(&jl8ijq*dg(^&!vy-omxp^sea9de6p=@%qx-ugw=s%!o'

DEBUG = False 

ALLOWED_HOSTS = [
    '0.0.0.0',
    '.takenexams.com',
    '.codelines.net',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'd4fqja4ae45vhs',
        'USER': 'tukbkkauppmrkb',
        'PASSWORD': 'fb26e0f7ce67790c24891ec81dd97644ed262903b874bf10dcc86a2bed77c096',
        'HOST': 'ec2-54-247-85-251.eu-west-1.compute.amazonaws.com',
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

