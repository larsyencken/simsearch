#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  simulate_search.py
#  simsearch
# 
#  Created by Lars Yencken on 03-09-2010.
#  Copyright 2010 Lars Yencken. All rights reserved.
#

"""
"""

import os
import sys
import optparse
import codecs

from simplestats import basic_stats 
from django.conf import settings
from consoleLog import withProgress

from simsearch.search import stroke, models

def simulate_search(output_file, strategy='greedy'):
    if strategy == 'greedy':
        search_fn = _greedy_search
    elif strategy == 'shortest':
        search_fn = _breadth_first_search
    else:
        raise ValueError(strategy)

    traces = []
    for query, target in withProgress(_load_search_examples()):
        path = search_fn(query, target)
        traces.append((query, target, path))

    _dump_traces(traces, output_file)

def _dump_traces(traces, filename):
    with codecs.open(filename, 'w', 'utf8') as ostream:
        for q, t, p in traces:
            if not p:
                print >> ostream, u'%s (%s) None' % (q, t)
                continue

            if p[-1] == t:
                p = p[:-1]
            else:
                t = u'(%s)' % t

            if p:
                print >> ostream, u'%s %s [%s]' % (q, t, ''.join(p))
            else:
                print >> ostream, u'%s %s []' % (q, t)

    print 'Paths dumped to %s' % filename

def _load_search_examples():
    flashcard_file = os.path.join(settings.DATA_DIR, 'similarity', 'flashcard')
    results = []
    with codecs.open(flashcard_file, 'r', 'utf8') as istream:
        for line in istream:
            _id, query, targets = line.split()
            for target in targets:
                results.append((query, target))

    return results

def _greedy_search(query, target, limit=5):
    """
    Simulate a search between the query and target.
    """
    path = [query]
    while path[-1] != target and len(path) <= limit:
        query = path[-1]
        neighbours = _get_neighbours(query)

        if target in neighbours:
            # Success!
            path.append(target)
        else:
            # Our options are neighbours we haven't tried yet
            options = neighbours.difference(path)

            if not options:
                # Search exhausted =(
                break

            # Choose the one visually most similar to the target
            _d, neighbour = min((sed(n, target), n) for n in options)
            path.append(neighbour)

    return path

def _breadth_first_search(query, target, limit=5):
    paths = [[query]]
    shortest = set([query]) # has a shortest path been checked
    while paths:
        current = paths.pop(0)
        query = current[-1]
        neighbours = _get_neighbours(query)

        if target in neighbours:
            current.append(target)
            return current

        if len(current) < limit:
            neighbours = sorted(neighbours, key=lambda n: sed(n, target))
            neighbours = [n for n in neighbours if n not in shortest]
            shortest.update(neighbours)
            paths.extend((current + [n]) for n in neighbours)

class cache(dict):
    def __init__(self, f):
        self.f = f

    def __call__(self, *args):
        if args not in self:
            self[args] = self.f(*args)

        return self[args]

@cache
def _get_neighbours(k):
    neighbours = set(n.kanji for n in models.Node.objects.get(
            pivot=k).neighbours[:settings.N_NEIGHBOURS_RECALLED])
    return neighbours

sed = cache(stroke.StrokeEditDistance())

#----------------------------------------------------------------------------#

def _create_option_parser():
    usage = \
"""%prog [options] output_file

Simulate queries through the search graph, dumping the traces to the given
file."""

    parser = optparse.OptionParser(usage)

    parser.add_option('--strategy', action='store', type='choice',
            choices=['greedy', 'shortest'], dest='strategy',
            default='greedy',
            help='The search strategy to use ([greedy]/shortest)')

    return parser

def main(argv):
    parser = _create_option_parser()
    (options, args) = parser.parse_args(argv)

    if len(args) != 1:
        parser.print_help()
        sys.exit(1)

    simulate_search(args[0], strategy=options.strategy)

#----------------------------------------------------------------------------#

if __name__ == '__main__':
    main(sys.argv[1:])

# vim: ts=4 sw=4 sts=4 et tw=78:
