from register.settings.common import *
import os


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
EMAIL_BACKEND = "sendgrid_backend.SendgridBackend"

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