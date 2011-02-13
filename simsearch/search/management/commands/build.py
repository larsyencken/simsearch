# -*- coding: utf-8 -*-
#
#  build.py
#  simsearch
# 
#  Created by Lars Yencken on 27-08-2010.
#  Copyright 2010 Lars Yencken. All rights reserved.
#

"""
Adds a command to automatically run a build for each app used.
"""

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

class Command(BaseCommand):
    help = 'Builds the initial similarity database.'

    def handle(self, *args, **kwargs):
        found_one = False
        for app_name in settings.INSTALLED_APPS:
            module = __import__(app_name)
            for part in app_name.split('.')[1:]:
                module = getattr(module, part)

            if hasattr(module, 'build'):
                module.build()
                found_one = True

        if not found_one:
            raise Exception('no apps had build commands')

# vim: ts=4 sw=4 sts=4 et tw=78:
