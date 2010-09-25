# -*- coding: utf-8 -*-
#
#  heap_cache.py
#  simsearch
# 
#  Created by Lars Yencken on 30-08-2010.
#  Copyright 2010 Lars Yencken. All rights reserved.
#

"""
Caches to aid similarity caculation, to efficiently maintain only the highest
similarity neighbours.
"""

import heapq

class TopNHeap(object):
    "A heap which only keeps the top-n items and their weights."
    __slots__ = '_n', '_backing_list'
    def __init__(self, n):
        self._n = n
        self._backing_list = []

    def add(self, item, weight):
        heapq.heappush(self._backing_list, (weight, item))
        if len(self._backing_list) > self._n:
            heapq.heappop(self._backing_list)

    def get_contents(self):
        return self._backing_list

class FixedSimilarityCache(object):
    """
    A kanji similarity cache which only keeps the top-n most similar
    neighbours.
    """
    def __init__(self, n):
        self._n = n
        self._heaps = {}
        self._sum = 0.0
        self._n_seen = 0.0
        self._sum_squared = 0.0

    def add(self, kanji_a, kanji_b, similarity):
        """
        Attempt to add this similarity score to the cache. If there are
        already n closer neighbours for either kanji it will be discarded.  
        """
        self.get_heap(kanji_a).add(kanji_b, similarity)
        self.get_heap(kanji_b).add(kanji_a, similarity)
        self._n_seen += 1
        self._sum += similarity
        self._sum_squared += similarity * similarity


    def __getitem__(self, kanji):
        return self.get_heap(kanji)

    def get_heap(self, kanji):
        heap = self._heaps.get(kanji)
        if heap is None:
            heap = self._heaps.setdefault(kanji, TopNHeap(self._n))
        return heap

    def get_mean(self):
        return self._sum / self._n_seen

# vim: ts=4 sw=4 sts=4 et tw=78:

