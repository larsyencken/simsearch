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
from django.utils import simplejson
from django.http import HttpResponse

from cjktools import scripts
from mongoengine.queryset import DoesNotExist

import models

def raw_search(request):
    context = {}
    kanji = request.GET.get('query') or ''
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

def old_search(request):
    return render_to_response('search/old.html', {},
            context_instance=RequestContext(request))

def old_search_xhr(request):
    pivot = request.GET.get('pivot')
    neighbours = [n.kanji for n in models.Node.objects.get(
            pivot=pivot).neighbours]
    response_dict = {
                'pivot_kanji': pivot,
                'tier1': neighbours[:4],
                'tier2': neighbours[4:9],
                'tier3': neighbours[9:],
            }
    return HttpResponse(
            simplejson.dumps(response_dict),
            mimetype='application/javascript',
        )

def _is_valid_query(kanji):
    return len(kanji) == 1 and scripts.script_type(kanji) == \
            scripts.Script.Kanji

# vim: ts=4 sw=4 sts=4 et tw=78:

