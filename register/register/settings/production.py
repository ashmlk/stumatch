from register.settings.common import *
import os
from urllib.parse import urlparse
import django_heroku

DEBUG = False

ALLOWED_HOSTS = ['corscope.heroku.com','wwww.corscope.com','corscope.com']

#EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
#EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')

redis_url = urlparse(os.environ.get('REDISTOGO_URL', 'redis://localhost:6959'))

CACHES = {
    'default': {
        'BACKEND': "django_redis.cache.RedisCache",
        'LOCATION': '%s:%s' % (redis_url.hostname, redis_url.port),
        'OPTIONS': {
            'DB': 0,
            'PASSWORD': redis_url.password,
        }
    }
}

CELERY_BROKER_URL=os.environ.get('REDISTOGO_URL')
CELERY_RESULT_BACKEND=os.environ.get('REDISTOGO_URL')
CELERY_BROKER_TRANSPORT_OPTIONS = {
    "max_connections": 2,
}

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

django_heroku.settings(locals())