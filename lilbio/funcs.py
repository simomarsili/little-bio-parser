# -*- coding: utf-8 -*-
# Author: Simone Marsili <simomarsili@gmail.com>
# License: BSD 3 clause
"""
Functions of sequences. If a transformed version of the sequence is
returned, it should be a list of symbols (not a string).
"""
import functools
import logging

logger = logging.getLogger(__name__)
# uppercase plus *,- symbols
GENERIC_ALPHABET = set('*-ABCDEFGHIJKLMNOPQRSTUVWXYZ')
# Canonical/natural codes plus gap symbol.
PROTEIN_ALPHABET = set('-ACDEFGHIKLMNPQRSTVWY')


def compose(*funcs):
    """Composition of functions from iterable.

    Functions operate in iteration order:
    compose([a, b])(x) == b(a(x)).
    """

    def gf(f, g):
        """Compose two functions."""
        return lambda x: g(f(x))

    return functools.reduce(gf, funcs, lambda x: x)


def from_alphabet_only(s, alphabet):
    """Filter symbols from alphabet."""
    return [c for c in s if c in alphabet]


def uppercase_only(s):
    """Filter uppercase + '-' symbols."""
    return from_alphabet_only(s, GENERIC_ALPHABET)


def tostr(s):
    """Stringify sequence s."""
    return ''.join(s)
