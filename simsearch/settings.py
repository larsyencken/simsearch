# -*- coding: utf-8 -*-
#
#  settings.py
#  simsearch
#
#  Created by Lars Yencken on 24-08-2010.
#  Copyright 2010 Lars Yencken. All rights reserved.
#

"""
Settings for the simsearch project.
"""

import os

import mongoengine

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

PROJECT_ROOT = os.path.dirname(__file__)

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/static/'

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

# static data files needed for building
DATA_DIR = os.path.join(PROJECT_ROOT, 'data')

# default stroke source
if STROKE_SOURCE is None:
    STROKE_SOURCE = os.path.join(DATA_DIR, 'strokes_ulrich')

# default frequency source
if FREQ_SOURCE is None:
    FREQ_SOURCE = os.path.join(DATA_DIR, 'jp_char_corpus_counts.gz')

# vim: ts=4 sw=4 sts=4 et tw=78:
