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

from django.views.static import serve 
from django.conf import settings

def media(request):
    """
    Use this to serve static media. Since some of the media may be files
    which were uploaded, we want to password protect everything.
    """
    return serve(request, request.path[len(settings.MEDIA_URL):],
            document_root=settings.MEDIA_ROOT)

# vim: ts=4 sw=4 sts=4 et tw=78:
