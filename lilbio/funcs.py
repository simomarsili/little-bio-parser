"""Filter/transform records."""
import functools
import numpy

# uppercase plus *,- symbols
GENERIC_ALPHABET = set('*-ABCDEFGHIJKLMNOPQRSTUVWXYZ')
# Canonical/natural codes plus gap symbol.
PROTEIN_ALPHABET = set('-ACDEFGHIKLMNPQRSTVWY')


def compose(*funcs):
    # compose a list of functions (right to left)
    def fg(f, g):
        return lambda recs: f(g(recs))
    return functools.reduce(fg, funcs, lambda recs: recs)


def as_list(a):
    for k, head, seq in a:
        yield k, head, list(seq)


def as_array(a):
    for k, head, seq in a:
        yield k, head, numpy.array(list(seq))


def hmm_positions(a):
    for k, head, seq in a:
        seq = ''.join([c for c in seq if c in GENERIC_ALPHABET])
        yield k, head, seq


def hmm_positions2(a):
    inds = None

    # a = as_array(a)

    def wrapped():
        nonlocal inds
        if inds is None:
            k, head, seq = next(a)
            seq = numpy.array(list(seq))
            inds = [j for j, c in enumerate(seq) if c in GENERIC_ALPHABET]
            seq = seq[inds]
            yield k, head, seq
        for k, head, seq in a:
            seq = numpy.array(list(seq))
            seq = seq[inds]
            yield k, head, seq

    return wrapped()
