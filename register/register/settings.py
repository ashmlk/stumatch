import os
from django.urls import reverse_lazy
from celery.schedules import crontab   

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_DIR = os.path.join(BASE_DIR,'templates')
#STATIC_DIR = os.path.join(BASE_DIR,'static/')
MEDIA_DIRS = [ 
             os.path.join(BASE_DIR,'media')
]
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'e2a&eyvw$gfs=8o)xzru2f@@7iiy-3+da18o#immnl7ln@3xm-'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

AUTH_USER_MODEL = 'main.Profile'

# Email confirmation
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Application definition

INSTALLED_APPS = [
    
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.postgres',
    'main',
    'home',
    'crispy_forms',
    'ckeditor',
    'taggit',
    'taggit_selectize',
    'dal',
    'dal_select2',
    'friendship',
    'django_celery_results',
    'stream_django',
    'django_celery_beat',
]

CRISPY_TEMPLATE_PACK = 'bootstrap4'

CKEDITOR_UPLOAD_PATH = 'uploads/files/'

TAGGIT_SELECTIZE = {
    'MINIMUM_QUERY_LENGTH': 1,
    'RECOMMENDATION_LIMIT': 8,
    'PERSIST': False,
    'OPEN_ON_FOCUS': False,
    'HIDE_SELECTED': True,
    'CLOSE_AFTER_SELECT': True,
    'LOAD_THROTTLE': 100,
    'SELECT_ON_TAB': True,
    'REMOVE_BUTTON': True,
}

TAGGIT_TAGS_FROM_STRING = 'taggit_selectize.utils.parse_tags'
TAGGIT_STRING_FROM_TAGS = 'taggit_selectize.utils.join_tags'

CKEDITOR_CONFIGS = {
'default': {
    'toolbar': [[ 'Source', '-', 'Save', 'NewPage', 'Preview', 'Print', '-', 'Templates' ],
                [ 'Cut', 'Copy', 'Paste', 'PasteText', 'PasteFromWord', '-', 'Undo', 'Redo' ],
                [ 'Find', 'Replace', '-', 'SelectAll', '-', 'Scayt' ],
                [ 'Bold', 'Italic', 'Underline', 'Strike', 'Subscript', 'Superscript', '-', 'CopyFormatting', 'RemoveFormat' ],
                [ 'NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'Blockquote', 'CreateDiv', '-', 'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock', '-', 'BidiLtr', 'BidiRtl', 'Language' ] ,
                [ 'Link', 'Unlink', 'Anchor' ],
                [ 'Image', 'Flash', 'Table', 'HorizontalRule', 'Smiley', 'SpecialChar', 'PageBreak', 'Iframe' ],
                [ 'Styles', 'Format', 'Font', 'FontSize' ],
                [ 'TextColor', 'BGColor' ],
                [ 'Maximize', 'ShowBlocks' ]],
    'width': 'auto',

          },
    }

#CELERY CONFIG

CELERY_BROKER_URL = 'redis://localhost:6379'
CELERY_BROKER_TRANSPORT = 'redis'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_IMPORTS = (
    'home.tasks',
)
CELERY_BEAT_SCHEDULE = {
    'update-hot-posts': {
        'task':'home.tasks.get_hot_posts',
        'schedule': 3600.0,
    },
    'update-top-posts': {
        'task':'home.tasks.get_top_posts',
        'schedule': 86400.0,
    },
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "IGNORE_EXCEPTIONS": True,  
        },
        "KEY_PREFIX": "redis_one"
    }
}

# STREAM CONFIG

CACHE_TTL = 60 * 15

STREAM_API_KEY = 'dec3nd9aasae'
STREAM_API_SECRET = '879qq6gqwk5rf5r53fgfqkye5np8n24wjwctvm55mzvrnnsqk4vpjrrggyz3a9r6'


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

SITE_ID = 1

ROOT_URLCONF = 'register.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR,],
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

WSGI_APPLICATION = 'register.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'register',
        'USER': 'root',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
STATIC_URL = '/static/'
LOGIN_URL = reverse_lazy('main:user_login')
LOGIN_REDIRECT_URL = reverse_lazy('home:home')
LOGOUT_REDIRECT_URL = reverse_lazy('main:user_login')


