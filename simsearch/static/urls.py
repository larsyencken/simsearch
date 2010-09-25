# -*- coding: utf-8 -*-
#
#  urls.py
#  simsearch
# 
#  Created by Lars Yencken on 14-09-2010.
#  Copyright 2010 Lars Yencken. All rights reserved.
#

"""
Urlconf for static pages.
"""

from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('simsearch.static.views',
    url(r'^help/$',     'help',     name='help'),
    url(r'^feedback/$', 'feedback', name='feedback'),
    url(r'^about/$',    'about',    name='about'),
)

# vim: ts=4 sw=4 sts=4 et tw=78:
