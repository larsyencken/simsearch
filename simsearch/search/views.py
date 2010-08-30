# -*- coding: utf-8 -*-
#
#  views.py
#  simsearch
# 
#  Created by Lars Yencken on 30-08-2010.
#  Copyright 2010 Lars Yencken. All rights reserved.
#

"""
"""

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib import messages

from cjktools import scripts
from mongoengine.queryset import DoesNotExist

import models

def search(request):
    context = {}
    kanji = request.GET.get('query')
    trace = request.GET.get('trace', '') + kanji
    context['query'] = kanji
    context['trace'] = trace

    if kanji:
        if _is_valid_query(kanji):
            try:
                node = models.Node.objects.get(pivot=kanji)
                context['results'] = node.neighbours
            except DoesNotExist:
                messages.add_message(request, messages.INFO,
                        'Sorry, no matching results for this query.')

        else:
            messages.add_message(request, messages.WARNING,
                    'The query should be a single kanji only.')

    return render_to_response('search/index.html', context,
            context_instance=RequestContext(request))

def _is_valid_query(kanji):
    return len(kanji) == 1 and scripts.script_type(kanji) == \
            scripts.Script.Kanji

# vim: ts=4 sw=4 sts=4 et tw=78:

