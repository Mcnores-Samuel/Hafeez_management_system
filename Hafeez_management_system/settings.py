"""
Django settings for Hafeez_management_system project.

Generated by 'django-admin startproject' using Django 4.2.6.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import os
import dj_database_url
import logging
logger = logging.getLogger('django.security.csrf')


logging.basicConfig(level=logging.INFO)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = (bool(int(os.environ.get('DEBUG', 1))))

MAIN_DOMAIN = os.environ.get('MAIN_DOMAIN')
SUBDOMAIN_NAME = os.environ.get('SUBDOMAIN_NAME')
SERVER_DOMAIN1 = os.environ.get('SERVER_DOMAIN', default=".vercel.app")
SERVER_DOMAIN2 = os.environ.get('SERVER_DOMAIN2', default=".railway.app")
OTHER_DOMAIN = os.environ.get('OTHER_DOMAIN')
ALLOWED_HOSTS = [MAIN_DOMAIN, SUBDOMAIN_NAME, SERVER_DOMAIN1,
                 SERVER_DOMAIN2, OTHER_DOMAIN, 'localhost', '127.0.0.1']

CSRF_COOKIE_SECURE = (bool(int(os.environ.get('CSRF_COOKIE_SECURE', 1))))

CSRF_TRUSTED_ORIGINS = [
    'https://' + MAIN_DOMAIN,
    'https://' + SUBDOMAIN_NAME,
    'http://' + MAIN_DOMAIN,
    'http://' + SUBDOMAIN_NAME
]
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'

USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

SESSION_COOKIE_SECURE = (bool(int(os.environ.get('SESSION_COOKIE_SECURE', 1))))
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'
SESSION_COOKIE_AGE = 60 * 60 * 24 * 7
# Application definition


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'system_core_1.apps.SystemCore1Config',
    'django_filters',
    'django_email_verification',
    'storages',
    'django_bootstrap5',
    'webpush',
]

WEBPUSH_SETTINGS = {
   "VAPID_PUBLIC_KEY": os.environ.get('VAPID_PUBLIC_KEY'),
   "VAPID_PRIVATE_KEY": os.environ.get('VAPID_PRIVATE_KEY'),
   "VAPID_ADMIN_EMAIL": os.environ.get('VAPID_ADMIN_EMAIL'),
}

MESSAGE_STORAGE = "django.contrib.messages.storage.cookie.CookieStorage"

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'system_core_1.middleware.RedirectAuthenticatedUsersMiddleware',
]

ROOT_URLCONF = 'Hafeez_management_system.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
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

WSGI_APPLICATION = 'Hafeez_management_system.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASE_URL = os.environ.get('DATABASE_URL')

DATABASES = {
    'default': dj_database_url.config(
        default=DATABASE_URL,
        conn_max_age=600,
    )
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = "Africa/Blantyre"

USE_I18N = True

USE_TZ = True


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'system_core_1.UserProfile'

def verified_callback(user):
    user.is_active = True

EMAIL_MAIL_CALLBACK = verified_callback

EMAIL_VERIFIED_CALLBACK = verified_callback
EMAIL_FROM_ADDRESS = os.environ.get('EMAIL_FROM_ADDRESS')
EMAIL_MAIL_SUBJECT = 'Confirm your email {{ user.username }}'
EMAIL_MAIL_HTML = 'authentication/activation_email.html'
EMAIL_MAIL_PLAIN = 'authentication/activation_email.txt'
EMAIL_MAIL_TOKEN_LIFE = 60 * 60
EMAIL_MAIL_PAGE_TEMPLATE = 'comfirm_template.html'
EMAIL_PAGE_DOMAIN = os.environ.get('EMAIL_PAGE_DOMAIN')
EMAIL_MULTI_USER = True


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_PORT = os.environ.get('EMAIL_PORT')
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')

PASSWORD_RESET_TIMEOUT_DAYS = 1
PASSWORD_RESET_EMAIL_SUBJECT = 'registration/reset_email_subject.txt'

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static'


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
    'default': {
        'BACKEND': 'django.core.files.storage.FileSystemStorage',
        'LOCATION': os.path.join(BASE_DIR, 'media'),
    },
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'WARNING',
    },
    'django': {
        'handlers': ['console'],
        'level': 'ERROR',
        'propagate': True,
    },
}
