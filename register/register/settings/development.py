from register.settings.common import *
import os


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
THUMBNAIL_DEBUG = True


'''
SENDGRID_API_KEY = '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'
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'app183550357@heroku.com'
EMAIL_HOST_PASSWORD = 'pxnz2ghd3106'
DEFAULT_FROM_EMAIL = 'JoinCampus Team <no-reply@joincampus.ca>'
'''

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

SITE_ID = 8

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

STATIC_URL = '/static/'
MEDIA_DIRS = [ 
             os.path.join(BASE_DIR, 'media')
]

STATICFILES_DIRS = [ 
    os.path.join(BASE_DIR, 'static')
]
STATIC_ROOT = os.path.join(BASE_DIR, 'live-static', 'static-root')
# Static files (CSS, JavaScript, Images)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')