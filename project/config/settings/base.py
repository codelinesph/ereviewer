import os

from config.vars import *

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# HTML_MINIFY = True

INSTALLED_APPS = [
    'core.apps.CoreConfig',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'guest',
    'student',
    'content.apps.ContentConfig',
    'users.apps.UsersConfig',
    'taken.apps.TakenConfig',
    'account.apps.AccountsConfig',

    'reports.admin_reports.apps.AdminReportsConfig',
    'codelines.studio.apps.StudioConfig',

    'nested_admin',
]
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'htmlmin.middleware.HtmlMinifyMiddleware',
    # 'htmlmin.middleware.MarkRequestMiddleware',
]
ROOT_URLCONF = 'config.urls'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, '../core/templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
WSGI_APPLICATION = 'config.wsgi.application'

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
    )
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# localization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Singapore'
USE_I18N = True
USE_L10N = True
USE_TZ = True

DEFAULT_QUERY_LIMIT = 10

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "../core/static")
]

STATIC_ROOT = os.path.join(BASE_DIR, '../staticfiles')