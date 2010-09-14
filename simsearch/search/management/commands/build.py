# -*- coding: utf-8 -*-
#
#  build.py
#  simsearch
# 
#  Created by Lars Yencken on 27-08-2010.
#  Copyright 2010 Lars Yencken. All rights reserved.
#

"""
"""

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

class Command(BaseCommand):
    help = 'Builds the initial similarity database.'

    def handle(self, *args, **kwargs):
        for app_name in settings.INSTALLED_APPS:
            app = __import__(app_name)
            if hasattr(app, 'build'):
                print app
                app.build()

# vim: ts=4 sw=4 sts=4 et tw=78:
