from register.settings.common import *
import os
from urllib.parse import urlparse
import django_heroku
import dj_database_url


DEBUG = False

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': ('%(asctime)s [%(process)d] [%(levelname)s] ' +
                       'pathname=%(pathname)s lineno=%(lineno)s ' +
                       'funcname=%(funcName)s %(message)s'),
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        }
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'testlogger': {
            'handlers': ['console'],
            'level': 'INFO',
        }
    }
}

ALLOWED_HOSTS = ['.herokuapp.com','wwww.corscope.com','.corscope.com']

#EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
#EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')


CACHES = {
    'default': {
        'BACKEND': "redis_cache.RedisCache",
        'LOCATION': os.environ.get('REDISTOGO_URL', 'redis://127.0.0.1:6379'), 
        "OPTIONS": {
            'DB': 0,
            "CLIENT_CLASS": "redis_cache.client.DefaultClient",
        }
    }
}
SITE_ID = 4

CELERY_BROKER_TRANSPORT_OPTIONS = {
    "max_connections": 2,
}

SECURE_SSL_REDIRECT = True

DEBUG_PROPAGATE_EXCEPTIONS = True

db_from_env = dj_database_url.config(conn_max_age=600)
DATABASES['default'].update(db_from_env)

SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY")
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('SENDGRID_USERNAME', '')
EMAIL_HOST_PASSWORD = os.environ.get('SENDGRID_PASSWORD', '')
DEFAULT_FROM_EMAIL = 'Corscope Team <no-reply@corscope.com>'

STATIC_URL = '/static/'
STATICFILES_DIRS = [ 
    os.path.join(BASE_DIR, 'static')
]
STATIC_ROOT = os.path.join(BASE_DIR, 'live-static', 'static-root')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=94608000',
}
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'

DEFAULT_FILE_STORAGE = 'register.storage_backends.MediaStorage'



