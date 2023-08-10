from .base import *

SECRET_KEY = '&7lhj(&jl8ijq*dg(^&!vy-omxp^sea9de6p=@%qx-ugw=s%!o'

DEBUG = True

ALLOWED_HOSTS = ["0.0.0.0","192.168.239.1","192.168.1.5","localhost"]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'database.sqlite3',
        'USER': 'root',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

# EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
# EMAIL_FILE_PATH = '/tmp/app-messages'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# EMAIL_HOST = 'sg3plcpnl0216.prod.sin3.secureserver.net'
# EMAIL_PORT = 465
# EMAIL_USE_SSL = True
# EMAIL_HOST_USER = 'accounts@takenexams.com'
# EMAIL_HOST_PASSWORD = 'Ch0lylshhFzdlTz*IW'

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.mailgun.org'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'postmaster@sandboxa61d79808c5f4b5799f6a4c7a0d3c709.mailgun.org'
EMAIL_HOST_PASSWORD = '4410cbe7c2368ba17305f67ec3180303-7caa9475-be6de639'

# EMAIL_USE_TLS = True
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_HOST_USER = 'codelines.net@gmail.com'
# EMAIL_HOST_PASSWORD = 'Cdln!@2018'
# EMAIL_PORT = 587


STATIC_URL = '/static/'

WEBDAV_URL = 'https://ur4ujkfophys@webdisk.takenexams.com/www/img-cdn/dev/'
WEBDAV_PUBLIC_URL = 'https://takenexams.com/img-cdn/dev/'

DEFAULT_FILE_STORAGE = 'django_webdav_storage.storage.WebDavStorage'
