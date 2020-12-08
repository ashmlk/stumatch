from register.settings.common import *
import os
from urllib.parse import urlparse
#import django_heroku
import dj_database_url
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))

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

ALLOWED_HOSTS = ['.herokuapp.com','wwww.joincampus.ca','.joincampus.ca']

#EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
#EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')

CACHES = {
    'default': {
        'BACKEND': "django_redis.cache.RedisCache",
        'LOCATION': os.environ.get('REDISTOGO_URL', 'redis://127.0.0.1:6379'), 
        "OPTIONS": {
            'DB': 0,
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}
SITE_ID = 6

CELERY_BROKER_TRANSPORT_OPTIONS = {
    "max_connections": 2,
}

SECURE_SSL_REDIRECT = True

DEBUG_PROPAGATE_EXCEPTIONS = True

db_from_env = dj_database_url.config(conn_max_age=600)
DATABASES['default'].update(db_from_env)


SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY')
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = os.environ.get('SENDGRID_USERNAME')
EMAIL_HOST_PASSWORD = os.environ.get('SENDGRID_PASSWORD')
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'JoinCampus Team <no-reply@joincampus.ca>'

STATIC_URL = '/static/'
STATICFILES_DIRS = [ 
    os.path.join(BASE_DIR, 'static')
]
STATIC_ROOT = os.path.join(BASE_DIR, 'live-static', 'static-root')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

AWS_S3_REGION_NAME = 'us-east-2'
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
#AWS_QUERYSTRING_AUTH = False # ckeditor
AWS_DEFAULT_ACL = None
AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400',}
DEFAULT_FILE_STORAGE = 'register.storage_backends.MediaStorage'
