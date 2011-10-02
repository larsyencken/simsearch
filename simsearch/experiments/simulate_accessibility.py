#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  simulate_accessibility.py
#  simsearch
# 
#  Created by Lars Yencken on 05-09-2010.
#  Copyright 2010 Lars Yencken. All rights reserved.
#

"""
A basic simulation of accessibility improvements estimated from use of visual
similarity search.
"""

import os
import sys
import optparse
import codecs
import random

from simplestats import FreqDist, basic_stats

from simsearch import settings
from simsearch.search import models

DEFAULT_THRESHOLD = 0.95

def simulate_accessibility(output_file, threshold=DEFAULT_THRESHOLD):
    print 'Loading frequency distribution'
    dist = FreqDist.from_file(settings.FREQ_SOURCE)

    print 'Loading kanji'
    kanji_set = list(models._get_kanji())
    random.seed(123456789)
    random.shuffle(kanji_set)

    kanji_in_order = sorted(kanji_set, key=lambda k: dist.prob(k))

    print 'Loading graph'
    graph = RestrictedGraph()

    print 'Dumping frequencies to %s' % os.path.basename(output_file)
    n_neighbours = []
    with codecs.open(output_file, 'w', 'utf8') as ostream:
        print >> ostream, u'#n_known,n_accessible'
        print >> ostream, u'%d,%d' % (0, 0)
        known_set = set()
        accessible_set = set()
        for i, kanji in enumerate(kanji_in_order):
            known_set.add(kanji)
            accessible_set.add(kanji)

            neighbours = graph[kanji]
            accessible_set.update(neighbours)
            n_neighbours.append(len(neighbours))

            if (i + 1) % 50 == 0:
                print >> ostream, u'%d,%d' % (len(known_set),
                        len(accessible_set))
        print >> ostream, u'%d,%d' % (len(known_set), len(accessible_set))

    print 'Average neighbourhood size: %.02f (σ = %.02f)' % \
            basic_stats(n_neighbours)

class RestrictedGraph(object):
    def __init__(self, threshold=DEFAULT_THRESHOLD):
        self._graph = models.Similarity.load()
        self._threshold = threshold

    def __getitem__(self, kanji):
        neighbour_heap = self._graph[kanji]
        ordered_neighbourhood = sorted(neighbour_heap.get_contents(),
                reverse=True)

        first_sim, first_neighbour = ordered_neighbourhood[0]
        cutoff_neighbours = set(n for (s, n) in ordered_neighbourhood
                if s >= self._threshold * first_sim)

        return cutoff_neighbours

#----------------------------------------------------------------------------#

def _create_option_parser():
    usage = \
"""%prog [options] output_file.csv

Simulates how many kanji are accessible as kanji are learned, assuming they
are studied in frequency order."""

    parser = optparse.OptionParser(usage)

    parser.add_option('-t', action='store', dest='threshold',
            default=DEFAULT_THRESHOLD, type='float',
            help='The neighbourhood cutoff threshold [%.02f]' % \
                    DEFAULT_THRESHOLD)

    return parser

def main(argv):
    parser = _create_option_parser()
    (options, args) = parser.parse_args(argv)

    if len(args) != 1:
        parser.print_help()
        sys.exit(1)

    simulate_accessibility(args[0], threshold=options.threshold)

#----------------------------------------------------------------------------#

if __name__ == '__main__':
    main(sys.argv[1:])

# vim: ts=4 sw=4 sts=4 et tw=78:
