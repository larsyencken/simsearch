# -*- coding: utf-8 -*-
#
#  context.py
#  simsearch
# 
#  Created by Lars Yencken on 04-09-2010.
#  Copyright 2010 Lars Yencken. All rights reserved.
#

"""
Context processors for similarity search.
"""

import os

from mercurial import ui, hg, node

def mercurial_revision():
    project_base = os.path.join(settings.PROJECT_ROOT, '..')
    repo = hg.repository(ui.ui(), project_base)
    fctx = repo.filectx(project_base, 'tip')

    return {'revision': {
                'short': node.short(fctx.node()),
                'number': fctx.rev(),
            }}

def site_settings():
    return {'settings': settings}

# vim: ts=4 sw=4 sts=4 et tw=78:
