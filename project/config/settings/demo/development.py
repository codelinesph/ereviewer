from config.settings.base import *

DEBUG = True

SECRET_KEY = '&7lhj(&jl8ijq*dg(^&!vy-omxp^sea9de6p=@%qx-ugw=s%!o'

ALLOWED_HOSTS = ["0.0.0.0","localhost"]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'py_ereviewer',
        'USER': 'root',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'd50abcvmcdthnj',
#         'USER': 'egywzjfmrwhmll',
#         'PASSWORD': 'e43dd9c0853a2257f2ec5d5f05fcc1b4b8857865b7d84ea03d1eb54ccdebbf2d',
#         'HOST': 'ec2-79-125-6-250.eu-west-1.compute.amazonaws.com',
#         'PORT': '5432',
#     }
# }

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.mailgun.org'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'postmaster@sandboxa61d79808c5f4b5799f6a4c7a0d3c709.mailgun.org'
EMAIL_HOST_PASSWORD = '4410cbe7c2368ba17305f67ec3180303-7caa9475-be6de639'

STATIC_URL = '/static/'

WEBDAV_URL = 'https://ur4ujkfophys@webdisk.takenexams.com/www/img-cdn/dev/'
WEBDAV_PUBLIC_URL = STATIC_URL + 'img/content/'

DEFAULT_FILE_STORAGE = 'django_webdav_storage.storage.WebDavStorage'