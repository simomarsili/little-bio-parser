# -*- coding: utf-8 -*-
# Copyright (C) 2016, Simone Marsili <simo.marsili@gmail.com>
# License: BSD 3 clause
"""Standard alphabets and utils for alphabet strings."""

import logging

__all__ = [
    "ALPHABETS",
    "alphabet_guess",
    "is_alphabet_compliant",
]

logger = logging.getLogger(__name__)

# uppercase plus *,- symbols
GENERIC_ALPHABET = '*-ABCDEFGHIJKLMNOPQRSTUVWXYZ'

# IUPAC/IUB Amino Acid/Nucleic Acid one letter codes.
IUPAC_PROTEIN_ALPHABET = '*-ABCDEFGHIJKLMNOPQRSTUVWXYZ'
IUPAC_NUCLEIC_ALPHABET = '-ABCDGHKMNRSTUVWY'
IUPAC_DNA_ALPHABET = '-ABCDGHKMNRSTVWY'
IUPAC_RNA_ALPHABET = '-ABCDGHKMNRSUVWY'

# Canonical/natural codes plus gap symbol.
PROTEIN_ALPHABET = '-ACDEFGHIKLMNPQRSTVWY'
NUCLEIC_ALPHABET = '-ACGTU'
DNA_ALPHABET = '-ACGT'
RNA_ALPHABET = '-ACGU'

ALPHABETS = (
    GENERIC_ALPHABET,
    PROTEIN_ALPHABET,
    DNA_ALPHABET,
    RNA_ALPHABET)


def _is_alphabet(string):
    """Check if `string` is a valid alphabet
    (an ordered string of symbols from GENERIC_ALPHABET).

    Parameters
    ----------
    string: str
        Alphabet string.

    Returns
    -------
    bool
        True if a valid alphabet.

    """
    try:
        chars = set(string)
        if chars <= set(GENERIC_ALPHABET) and string == ''.join(sorted(chars)):
            return True
    except TypeError:
        logger.exception('%r is not an alphabet string', string)

    return False


def _alphabet_score(alphabet, counts):
    """Score `alphabet` given frequency of symbols in `counts`.

    (adapted frm https://github.com/WebLogo/weblogo/blob/master/corebio/seq.py)
    Parameters
    ----------
    alphabet : str

    counts : dict-like
        Frequencies.

    Returns
    -------
    score : float

    """
    import math

    if _is_alphabet(alphabet):
        chars = set(alphabet) - set('*-')
        score = (sum([counts.get(a, 0) for a in chars]) /
                 math.log(len(alphabet)))
        logger.debug('alphabet score %r', score)
        return score
    else:
        return 0.0


def is_alphabet_compliant(sequences, alphabet):
    """Check wether `sequences` are `alphabet` compliant.

    Parameters
    ----------
    sequences : iterable

    alphabet : str

    Returns
    -------
    bool
        True if all sequences takes symbols from alphabet

    """
    return set().union(*sequences) <= set(alphabet)


def alphabet_guess(sequences):
    """Guess an alphabet for sequences.

    Parameters
    ----------
    sequences : iterable

    Returns
    -------
    guess : string
        alphabet with the highest score.

    See also
    --------
    lilbio.alphabets._alphabet_score

    """
    counts = _freqs(sequences)
    scores = [_alphabet_score(a, counts) for a in ALPHABETS]
    guess = ALPHABETS[scores.index(max(scores))]
    logging.info('Alphabet guess: %r', guess)
    return guess


def _freqs(sequences):
    """Return dict of frequencies for symbols in `sequences`.

    Parameters
    ----------
    sequences : iterable

    Returns
    -------
    counts : collections.Counter

    """
    import collections
    counts = collections.Counter()
    for seq in sequences:
        counts.update(seq)
    return counts
