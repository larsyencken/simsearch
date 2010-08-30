# -*- coding: utf-8 -*-
#
#  models.py
#  simsearch
# 
#  Created by Lars Yencken on 28-08-2010.
#  Copyright 2010 Lars Yencken. All rights reserved.
#

"""
Database models for similarity search.
"""

import os
import codecs
import gzip

from django.conf import settings
import mongoengine
import pkg_resources
from cjktools import scripts
from simplestats import comb
from nltk.probability import FreqDist, LaplaceProbDist

import stroke
import heap_cache

class Similarity(mongoengine.Document):
    "Raw similarity scores for kanji pairs."
    kanji_pair = mongoengine.StringField(max_length=2, primary_key=True)
    similarity = mongoengine.FloatField(min_value=0.0, max_value=1.0,
            required=True)

    def partner_to(self, kanji):
        "Returns the partnering kanji in this pair."
        if kanji not in self.kanji_pair:
            raise ValueError('kanji not part of this pair')

        return self.kanji_pair.replace(kanji, '')

    @classmethod
    def build(cls):
        cls.drop_collection()
        sed = stroke.StrokeEditDistance()
        kanji_set = _get_kanji()

        cache = heap_cache.FixedSimilarityCache(settings.N_NEIGHBOURS_STORED)
        for kanji_a, kanji_b in comb.unique_tuples(kanji_set):
            distance = sed(kanji_a, kanji_b)
            cache.add(kanji_a, kanji_b, 1 - distance)

        for kanji in kanji_set:
            heap = cache.get_heap(kanji)
            for similarity, neighbour in heap.get_contents():
                kanji_pair = ''.join(min(
                        (kanji, neighbour), (neighbour, kanji)
                    ))
                doc = Similarity(
                        kanji_pair=kanji_pair,
                        similarity=similarity,
                    )
                doc.save()

        return cache

    @classmethod
    def load(cls, n=None):
        if n is None:
            n = settings.N_NEIGHBOURS_STORED
        cache = heap_cache.FixedSimilarityCache(n)
        for record in cls.objects:
            kanji_pair = record.kanji_pair
            cache.add(kanji_pair[0], kanji_pair[1], record.similarity)

        return cache

    def __unicode__(self):
        return u'(%s, %s, %f)' % (self.kanji_pair[0], self.kanji_pair[1],
                self.similarity)

class Neighbour(mongoengine.EmbeddedDocument):
    "A weighted graph edge."
    kanji = mongoengine.StringField(max_length=1)
    weight = mongoengine.FloatField(min_value=0.0, max_value=1.0)

class Node(mongoengine.Document):
    """
    A single node in the state graph for Q-learning. The neighbours attribute
    stores Q(n, a) for all actions which can be taken from this node.
    """
    pivot = mongoengine.StringField(max_length=1, primary_key=True)
    neighbours = mongoengine.ListField(mongoengine.EmbeddedDocumentField(
            Neighbour))
    n_updates = mongoengine.IntField(default=0, min_value=0)

    @classmethod
    def build(cls, cache=None):
        "Builds the initial graph for Q learning."
        n = settings.N_NEIGHBOURS_RECALLED

        if cache is None:
            cache = Similarity.load(n)

        cls.drop_collection()
        dist = cls._load_corpus_counts()
        for kanji in _get_kanji():
            node = Node(pivot=kanji, neighbours=[])

            weights = {}
            for weight, partner in cache.get_heap(kanji).get_contents():
                weights[partner] = weight * dist.prob(partner)
            total_weights = sum(weights.itervalues())

            for partner, weight in sorted(weights.iteritems(),
                    key=lambda p: p[1], reverse=True):
                node.neighbours.append(Neighbour(kanji=partner,
                        weight=weight / total_weights))
            
            node.save()

    @classmethod
    def _load_corpus_counts(cls):
        input_file = os.path.join(settings.DATA_DIR,
                'corpus', 'jp_char_corpus_counts.gz')
        freq_dist = FreqDist()
        with open(input_file, 'r') as istream:
            istream = gzip.GzipFile(fileobj=istream)
            istream = codecs.getreader('utf8')(istream)
            for line in istream:
                kanji, count = line.split()
                freq_dist.inc(kanji, count=int(count))

        return LaplaceProbDist(freq_dist)

class Trace(mongoengine.Document):
    "A search path through the graph, as taken by a user."
    ip_address = mongoengine.StringField(max_length=15)
    path = mongoengine.ListField(mongoengine.StringField(max_length=1))

def build():
    "Builds the database."
    cache = Similarity.build()
    Node.build(cache)

#----------------------------------------------------------------------------#

def _get_kanji():
    "Fetches our canonical list of kanji to work with."
    if not hasattr(_get_kanji, '_cached'):
        istream = pkg_resources.ResourceManager().resource_stream(
                'cjktools_data', 'lists/char/jp_jyouyou')
        istream = codecs.getreader("utf8")(istream)

        kanji = scripts.unique_kanji(istream.read())
        _get_kanji._cached = kanji

    return _get_kanji._cached

#----------------------------------------------------------------------------#

if __name__ == '__main__':
    build()

# vim: ts=4 sw=4 sts=4 et tw=78:
