# -*- coding: utf-8 -*-
#
#  urls.py
#  simsearch
# 
#  Created by Lars Yencken on 31-08-2010.
#  Copyright 2010 Lars Yencken. All rights reserved.
#

"""
Urlconf for search app.
"""

from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('simsearch.search.views',
    url(r'^raw/$',      'raw_search',       name='raw_search'),
    url(r'^$',          'old_search',       name='old_search'),
    url(r'^old/xhr/$',  'old_search_xhr',   name='old_search_xhr'),
)

# vim: ts=4 sw=4 sts=4 et tw=78:

