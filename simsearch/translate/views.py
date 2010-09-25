# -*- coding: utf-8 -*-
#
#  views.py
#  simsearch
# 
#  Created by Lars Yencken on 11-09-2010.
#  Copyright 2010 Lars Yencken. All rights reserved.
#

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import Http404

import models

def translate(request, kanji=None):
    if kanji is None:
        raise Http404

    t = models.Translation.objects.get(kanji=kanji)
    if t is None:
        raise Http404

    return render_to_response('translate/kanji.html', {'translation': t},
            RequestContext(request))

# vim: ts=4 sw=4 sts=4 et tw=78:
