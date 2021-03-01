# CONTAINS SETTINGS FOR PRODUCTION

from .base import *
import ast

SECRET_KEY = config('SECRET_KEY')

DEBUG = config("DEBUG", cast=bool)

ALLOWED_HOSTS = ast.literal_eval(config("ALLOWED_HOSTS"))

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'NAME': config("DB_NAME"),
        'ENGINE': 'mysql.connector.django',
        'USER': config("DB_USER"),
        'PASSWORD': config("DB_PASS"),
        'HOST': config("DB_HOST"),
        'OPTIONS': {
            'autocommit': True,
        },
    }
}

# EMAIL SETTINGS

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_USE_TLS = config("EMAIL_USE_TLS", cast=bool)
# EMAIL_USE_SSL = config("EMAIL_USE_SSL", cast=bool)
EMAIL_HOST = config("EMAIL_HOST")
EMAIL_HOST_USER = config("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD")
EMAIL_PORT = config("EMAIL_PORT", cast=int)

DEFAULT_FROM_EMAIL = config("SENDER_EMAIL")
ADMINS_EMAIL = ast.literal_eval(config("ADMINS_EMAIL"))


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_ROOT = config("STATIC_ROOT")
STATIC_URL = '/static/'

MEDIA_ROOT = config("MEDIA_ROOT")
MEDIA_URL = '/media/'

TEMP_ROOT = config("TEMP_ROOT")

STATICFILES_DIRS = [BASE_DIR+"/static", ]
