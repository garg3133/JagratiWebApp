# CONTAINS SETTINGS FOR PRODUCTION

from .base import *
import ast

SECRET_KEY = config('DJANGO_SECRET_KEY_JAGRATI')

DEBUG = config("DEBUG", cast=bool)

ALLOWED_HOSTS = ast.literal_eval(config("ALLOWED_HOSTS"))

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# EMAIL SETTINGS

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = config("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD")
EMAIL_PORT = 587

DEFAULT_FROM_EMAIL = config("SENDER_EMAIL")
ADMINS_EMAIL = ast.literal_eval(config("ADMINS_EMAIL"))


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, '..', 'staticfiles/')
STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, '..', 'media/')
MEDIA_URL = '/media/'

TEMP_ROOT = os.path.join(BASE_DIR, '..', 'temp/')

STATICFILES_DIRS = [BASE_DIR+"/static", ]
