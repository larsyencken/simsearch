# -*- coding: utf-8 -*-
#
#  models.py
#  simsearch
# 
#  Created by Lars Yencken on 11-09-2010.
#  Copyright 2010 Lars Yencken. All rights reserved.
#

"""
A basic database model for a kanji-level dictionary.
"""

from simsearch import settings
from cjktools.resources import kanjidic
import mongoengine

class Translation(mongoengine.Document):
    "A per-kanji dictionary entry of readings and translations."
    kanji = mongoengine.StringField(max_length=1, primary_key=True)
    on_readings = mongoengine.ListField(mongoengine.StringField())
    kun_readings = mongoengine.ListField(mongoengine.StringField())
    glosses = mongoengine.ListField(mongoengine.StringField())

    @classmethod
    def build(cls):
        cls.drop_collection()
        kjd = kanjidic.Kanjidic()
        for entry in kjd.itervalues():
            translation = cls(
                    kanji=entry.kanji,
                    on_readings=entry.on_readings,
                    kun_readings=entry.kun_readings,
                    glosses = entry.gloss,
                )
            translation.save()

if __name__ == '__main__':
    Translation.build()

# vim: ts=4 sw=4 sts=4 et tw=78:
