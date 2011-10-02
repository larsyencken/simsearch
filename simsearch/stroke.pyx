# -*- coding: utf-8 -*-
#
#  stroke.pyx
#  simsearch
# 
#  Created by Lars Yencken on 03-09-2010.
#  Copyright 2010 Lars Yencken. All rights reserved.
#

"""
Optimised Levenstein distance calculation between stroke signatures for two
kanji.
"""

import os

from cjktools.common import sopen

from simsearch import settings

cdef class StrokeEditDistance:
    """The edit distance between stroke sequences for both kanji."""
    cdef readonly signatures
    cdef readonly object stroke_types
    cdef readonly int n_stroke_types

    def __init__(self, input_file=None):
        self.stroke_types = {}
        self.n_stroke_types = 0

        input_file = input_file or settings.STROKE_SOURCE
        self.signatures = {}
        i_stream = sopen(input_file)
        for i, line in enumerate(i_stream):
            kanji, raw_strokes = line.rstrip().split()
            raw_strokes = raw_strokes.split(',')
            strokes = map(self.get_stroke_type, raw_strokes)
            self.signatures[kanji] = strokes
        i_stream.close()

    def get_stroke_type(self, stroke):
        try:
            return self.stroke_types[stroke]
        except KeyError:
            pass

        self.stroke_types[stroke] = self.n_stroke_types
        self.n_stroke_types = self.n_stroke_types + 1

        return self.n_stroke_types - 1
    
    def raw_distance(self, kanji_a, kanji_b):
        s_py = self.signatures[kanji_a]
        t_py = self.signatures[kanji_b]

        return edit_distance(s_py, t_py)

    def __call__(self, kanji_a, kanji_b):
        s_py = self.signatures[kanji_a]
        t_py = self.signatures[kanji_b]

        result = edit_distance(s_py, t_py)
        return float(result) / max(len(s_py), len(t_py))
    
    def __contains__(self, kanji):
        return kanji in self.signatures

#----------------------------------------------------------------------------#

cdef edit_distance(s_py, t_py):
    cdef int m, n, i, j
    cdef int table[100][100]
    cdef int s[100]
    cdef int t[100]
    cdef int up, left, diag, cost

    s_len = len(s_py)
    t_len = len(t_py)
    if s_len > 99 or t_len > 99:
        raise ValueError, "stroke sequences too long"

    for 0 <= i < s_len:
        table[i][0] = i
        s[i] = s_py[i]
    table[s_len][0] = s_len

    for 0 <= j < t_len:
        table[0][j] = j
        t[j] = t_py[j]
    table[0][t_len] = t_len

    for 1 <= i <= s_len:
        for 1 <= j <= t_len:
            if s[i-1] == t[j-1]:
                cost = 0
            else:
                cost = 1

            up = table[i-1][j] + 1
            left = table[i][j-1] + 1
            diag = table[i-1][j-1] + cost
            if up <= left:
                if up <= diag:
                    table[i][j] = up
                else:
                    table[i][j] = diag
            else:
                if left <= diag:
                    table[i][j] = left
                else:
                    table[i][j] = diag

    return table[s_len][t_len]

# vim: ts=4 sw=4 sts=4 et tw=78:
