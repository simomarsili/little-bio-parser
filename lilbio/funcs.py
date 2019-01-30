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
        return lambda x: g(f(x))

    return functools.reduce(gf, funcs, lambda x: x)


def is_alphabet_compliant(s, alphabet):
    return all([c in alphabet for c in s])


def only_from_alphabet(s, alphabet):
    return [c for c in s if c in alphabet]


def only_hmm(s):
    return only_from_alphabet(s, GENERIC_ALPHABET)


def tostr(s):
    return ''.join(s)
