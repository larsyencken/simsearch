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
import itertools

from django.conf import settings
import mongoengine
from cjktools import scripts
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
        print 'Building similarity matrix'
        cls.drop_collection()
        sed = stroke.StrokeEditDistance()
        kanji_set = _get_kanji()

        cache = heap_cache.FixedSimilarityCache(settings.N_NEIGHBOURS_STORED)
        pairs = ((a, b) for (a, b) in itertools.product(kanji_set, kanji_set)
                if (a < b))
            
        for kanji_a, kanji_b in pairs:
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
    weight = mongoengine.FloatField(min_value=0.0)

    def __cmp__(self, rhs):
        return cmp(self.weight, rhs.weight)

    def __unicode__(self):
        return self.kanji

class Node(mongoengine.Document):
    """
    A single node in the state graph for Q-learning. The neighbours attribute
    stores Q(n, a) for all actions which can be taken from this node.
    """
    pivot = mongoengine.StringField(max_length=1, primary_key=True)
    neighbours = mongoengine.ListField(mongoengine.EmbeddedDocumentField(
            Neighbour))
    n_updates = mongoengine.IntField(default=0, min_value=0)

    def at(self, kanji):
        "Gets the neighbour described by the given kanji."
        for neighbour in self.neighbours:
            if neighbour.kanji == kanji:
                return neighbour

        raise KeyError(kanji)

    @classmethod
    def build(cls, cache=None):
        "Builds the initial graph for Q learning."
        print 'Building neighbourhood graph'
        n = settings.N_NEIGHBOURS_RECALLED

        if cache is None:
            cache = Similarity.load(n)

        cls.drop_collection()
        dist = cls._load_corpus_counts()
        for kanji in _get_kanji():
            node = Node(pivot=kanji, neighbours=[])

            weights = {}
            best_n = sorted(cache.get_heap(kanji).get_contents(),
                    reverse=True)[:n]
            for weight, partner in best_n:
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

    @classmethod
    def get_coverage(cls):
        "Returns the set of kanji for which neighbours are stored."
        db = cls.objects._collection
        return set(r['_id'] for r in db.find({}, fields=['_id']))

    @classmethod
    def update(cls, path):
        nodes = cls.objects.filter(pivot__in=list(path))
        if len(nodes) != len(path):
            raise ValueError('path not found in database')

        # cache Q(s, a) for the subgraph we're interested in
        q = cls._cache_subgraph(nodes)

        # Calculate Q'(s, a) in reverse order along the path
        # Q'(s, a) = (1 - A(s))Q(s, a) + A(s)*(r(a) + G * max_a Q(s', a))
        gamma = settings.UPDATE_GAMMA
        for i in xrange(len(path) - 2, -1, -1):
            s = path[i]
            q_s = q[s]
            alpha = 1.0 / (4.0 + 0.5 * q_s.n_updates)
            
            # update very action available from state s
            for a in sorted(q_s.neighbours, key=lambda n: n.weight,
                    reverse=True):
                q_old = a.weight

                r_a = (1 if a.kanji == path[-1] else 0)
                q_opt = r_a + gamma * max(q[a.kanji].neighbours).weight
                
                a.weight = (1.0 - alpha) * q_old + alpha * q_opt
                print u"Q(%s, %s): %.02f --> %0.02f" % (s, a.kanji, q_old,
                        a.weight)

            q_s.n_updates += 1
            q_s.save()

    @classmethod
    def _cache_subgraph(cls, nodes):
        q = {}
        missing_neighbours = set()
        for node in nodes:
            q[node.pivot] = node
            missing_neighbours.update(n.kanji for n in node.neighbours)
        missing_neighbours.discard(node.pivot for node in nodes)

        extra_nodes = cls.objects.filter(pivot__in=missing_neighbours)
        if len(extra_nodes) != len(missing_neighbours):
            raise ValueError('cannot cache subgraph -- neighbours missing')

        for node in extra_nodes:
            q[node.pivot] = node

        return q

    def __unicode__(self):
        return self.pivot

class Trace(mongoengine.Document):
    "A search path through the graph, as taken by a user."
    ip_address = mongoengine.StringField(max_length=15)
    path = mongoengine.ListField(mongoengine.StringField(max_length=1))

    @classmethod
    def log(cls, request, path):
        ip = request.META['REMOTE_ADDR']
        cls(ip_address=ip, path=list(path)).save()

def build():
    "Builds the database."
    cache = Similarity.build()
    Node.build(cache)

#----------------------------------------------------------------------------#

def _get_kanji():
    "Fetches our canonical list of kanji to work with."
    if not hasattr(_get_kanji, '_cached'):
        kanji_set = set()
        with codecs.open(settings.STROKE_SOURCE, 'r', 'utf8') as istream:
            for line in istream:
                kanji, rest = line.split()
                
                # check for a kanji or hanzi; our Chinese data extends into
                # the E000-F8FF private use block, so an "Unknown" script is
                # ok too
                assert len(kanji) == 1 and scripts.script_type(kanji) in \
                        (scripts.Script.Kanji, scripts.Script.Unknown)

                kanji_set.add(kanji)

        _get_kanji._cached = kanji_set

    return _get_kanji._cached

#----------------------------------------------------------------------------#

if __name__ == '__main__':
    build()

# vim: ts=4 sw=4 sts=4 et tw=78:
