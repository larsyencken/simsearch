# -*- coding: utf-8 -*-
#
#  views.py
#  simsearch
# 
#  Created by Lars Yencken on 14-09-2010.
#  Copyright 2010 Lars Yencken. All rights reserved.
#

"""
Static page views.
"""

from django.shortcuts import render_to_response
from django.template import RequestContext

def help(request):
    return render_to_response("static/help.html", {},
            context_instance=RequestContext(request))

def feedback(request):
    return render_to_response("static/feedback.html", {},
            context_instance=RequestContext(request))

def about(request):
    return render_to_response("static/about.html", {},
            context_instance=RequestContext(request))

# vim: ts=4 sw=4 sts=4 et tw=78:

