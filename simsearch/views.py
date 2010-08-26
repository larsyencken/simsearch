# -*- coding: utf-8 -*-
#
#  views.py
#  simsearch
# 
#  Created by Lars Yencken on 24-08-2010.
#  Copyright 2010 Lars Yencken. All rights reserved.
#

"""
"""

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.http import Http404

from jp_grapheme_alt.models import GraphemeAlternation

def search(request):
    if request.method != 'get' or 'path' != request.GET:
        raise Http404

    path = request.GET['path'].split(',')
    
# vim: ts=4 sw=4 sts=4 et tw=78:
