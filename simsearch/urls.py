# -*- coding: utf-8 -*-
#
#  urls.py
#  simsearch
# 
#  Created by Lars Yencken on 24-08-2010.
#  Copyright 2010 Lars Yencken. All rights reserved.
#

from django.conf.urls.defaults import *
from django.conf import settings

_patterns = ['',
    (r'^translate/', include('simsearch.translate.urls')),
    (r'', include('simsearch.static.urls')),
    (r'', include('simsearch.search.urls')),
]

if settings.DEBUG:
    _patterns[1:1] = [
        url(r'^media/', 'simsearch.views.media', name='media'),
    ]

urlpatterns = patterns(*_patterns)

# vim: ts=4 sw=4 sts=4 et tw=78:
