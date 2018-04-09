"""
Django settings for PBLExchangeDjango project.

Generated by 'django-admin startproject' using Django 1.11.4.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '4bw!xfvafdoc^8qkn*ix*i3)ndc9^k3_7*mkm&5d3t0)7ns#&='

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

PBL_VERSION = "1.0-dev"

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'pblexchange.apps.PblexchangeConfig',
    'pble_questions',
    'ckeditor',
    'ckeditor_uploader',
    'django_cas_ng',
    'pble_users',
    'pble_subscriptions'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'PBLExchangeDjango.middleware.LoginRequiredMiddleware',
]

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'PBLExchangeDjango.custom_CASBackend.CustomCASBackend',
)

ROOT_URLCONF = 'PBLExchangeDjango.urls'

# Mail settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'GideonBlegmand@gmail.com'
# SECURITY WARNING: keep the password private!
EMAIL_HOST_PASSWORD = ''
EMAIL_PORT = 587

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,  'templates')],
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

WSGI_APPLICATION = 'PBLExchangeDjango.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = 'static/'

MEDIA_URL = '/media/'
MEDIA_ROOT = 'media/'


# PBLE Defaults
PBLE_DEFAULT_SETTINGS = {
    'question_up_vote_points': '5',
    'answer_up_vote_points': '10',
    'comment_up_vote_points': '2',
    'question_down_vote_points': '-2',
    'answer_down_vote_points': '-2',
    'comment_down_vote_points': '-1',
    'accepted_answer_points': '15',
    'accepted_answer_acceptor_points': '2'
}

# CKEditor upload settings
CKEDITOR_UPLOAD_PATH = 'uploads/'

# Login settings
LOGIN_URL = 'login'
EXEMPT_USERS = ['aklost11', 'gblegm13']
DISALLOWED_DOMAINS = ['student.aau.dk']

# Login redirect
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'

# Django-cas-ng settings
CAS_SERVER_URL = 'https://login.aau.dk/cas/'
CAS_VERSION = 'CAS_2_SAML_1_0'
CAS_APPLY_ATTRIBUTES_TO_USER = True
