# -*- coding: utf-8 -*-
#
#  urls.py
#  simsearch
# 
#  Created by Lars Yencken on 24-08-2010.
#  Copyright 2010 Lars Yencken. All rights reserved.
#

from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('simsearch.search.views',
    (r'^$', 'search'),
    # Example:
    # (r'^simsearch/', include('simsearch.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
)

# vim: ts=4 sw=4 sts=4 et tw=78:
