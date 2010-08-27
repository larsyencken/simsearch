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
import pkg_resources
from cjktools import scripts
from simplestats import comb
import codecs

import pymongo

from simsearch.search import stroke 

class Command(BaseCommand):
    help = 'Builds the initial similarity database.'

    def handle(self, *args, **kwargs):
        ""
        istream = pkg_resources.ResourceManager().resource_stream(
                'cjktools_data', 'lists/char/jp_jyouyou')
        istream = codecs.getreader("utf8")(istream)

        kanji = scripts.unique_kanji(istream.read())

        similarity = pymongo.Connection().simsearch.similarity
        similarity.ensure_index('kanji_a')
        similarity.ensure_index('kanji_b')

        sed = stroke.StrokeEditDistance()

        i = 0
        for kanji_a, kanji_b in comb.unique_tuples(kanji):
            distance = sed(kanji_a, kanji_b)
            similarity.save({
                        '_id': i,
                        'kanji_a': kanji_a,
                        'kanji_b': kanji_b,
                        'similarity': 1 - sed(kanji_a, kanji_b),
                    })
            i += 1

# vim: ts=4 sw=4 sts=4 et tw=78:
