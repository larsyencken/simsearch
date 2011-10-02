# -*- coding: utf-8 -*-
#
#  settings.py
#  simsearch
# 
#  Created by Lars Yencken on 24-08-2010.
#  Copyright 2010 Lars Yencken. All rights reserved.
#

"""
Django settings for the simsearch project.
"""

import os

import mongoengine

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Lars Yencken', 'lars@yencken.org'),
)

MANAGERS = ADMINS

# normal django database access ignored
DATABASES = {
#    'default': {
#        'ENGINE': 'django_mongodb_engine.mongodb',
#        'NAME': 'simsearch',
#        'USER': '',
#        'PASSWORD': '',
#        'HOST': 'localhost',
#        'PORT': 27017,
#        'SUPPORTS_TRANSACTIONS': False,
#    },
}

# custom MongoDB connection settings
MONGODB_NAME = 'simsearch'
MONGODB_USERNAME = None
MONGODB_PASSWORD = None
MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017

UTF8_BYTES_PER_CHAR = 3 # for CJK chars

N_NEIGHBOURS_STORED = 100

N_NEIGHBOURS_RECALLED = 15

GOOGLE_ANALYTICS_CODE = None

# Tradeoff in Pr(a|s) and likelihood of reaching a further target from s'
UPDATE_GAMMA = 0.7

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Melbourne/Australia'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

PROJECT_ROOT = os.path.dirname(__file__)

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/static/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/admin/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '+-_s&+=m0+bc*$40jf1s#9x(ar=vom5(lt9=&*ol$)co*u(38r'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.contrib.messages.context_processors.messages",
    'simsearch.context.mercurial_revision',
    'simsearch.context.site_settings',
)

MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

SESSION_ENGINE = 'mongoengine.django.sessions'

ROOT_URLCONF = 'simsearch.urls'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_ROOT, 'templates'),
)

INSTALLED_APPS = (
#    'django.contrib.messages',
    'django.contrib.sessions',
    'djangotoolbox',
    'simsearch.search',
    'simsearch.translate',
    'simsearch.static',
)

# The source of stroke data for each character
STROKE_SOURCE = None

# The source of frequency counts for each character
FREQ_SOURCE = None

try:
    from local_settings import *
except ImportError:
    pass

# connect to our database
import mongoengine
mongoengine.connect(MONGODB_NAME, username=MONGODB_USERNAME,
        password=MONGODB_PASSWORD, host=MONGODB_HOST, port=MONGODB_PORT)

# default stroke source
if STROKE_SOURCE is None:
    STROKE_SOURCE = os.path.join(DATA_DIR, 'structure', 'strokes_ulrich')
    
# default frequency source
if FREQ_SOURCE is None:
    FREQ_SOURCE = os.path.join(DATA_DIR, 'corpus', 'jp_char_corpus_counts.gz')

# vim: ts=4 sw=4 sts=4 et tw=78:
