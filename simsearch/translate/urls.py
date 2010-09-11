# -*- coding: utf-8 -*-
#
#  urls.py
#  simsearch
# 
#  Created by Lars Yencken on 11-09-2010.
#  Copyright 2010 Lars Yencken. All rights reserved.
#

"""
Urlconf for translate app.
"""

from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('simsearch.translate.views',
    url(r'^(?P<kanji>.)/$', 'translate', name='translate_kanji'),
)

# vim: ts=4 sw=4 sts=4 et tw=78:

