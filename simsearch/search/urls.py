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
    url(r'^$',                      'search',       name='search_index'),
    url(r'^xhr/$',                  'search_json',  name='search_json'),
    url(r'^xhr/(?P<pivot>.*)/$',    'search_json',  name='search_json_kanji'),
    url(r'^target/$',               'translate',    name='search_target'),
    url(r'^target/(?P<kanji>.*)/$', 'translate',    name='search_target_kanji'),
)

# vim: ts=4 sw=4 sts=4 et tw=78:

