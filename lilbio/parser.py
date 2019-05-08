# -*- coding: utf-8 -*-
# Author: Simone Marsili <simomarsili@gmail.com>
# License: BSD 3 clause
"""alignment parser"""
import logging
import sys

import gopen

import lilbio

logger = logging.getLogger(__name__)


class LilBioError(Exception):
    """Base class for lilbio exceptions."""


class UnsupportedFormatError(LilBioError):
    """Unsupported format."""


class NotCallableError(LilBioError):
    """Argument func did not receive a callable object."""


def parse(source, fmt, func=None):
    """
    Parse an alignment file into records.

    Parameters
    ----------
    source : {str, file object}
        Alignment filename of a file handle.
    fmt : str
        Format of the alignment file.
        Valid values are: {'fasta', 'stockholm'}
    func : callable or iterable
        When passed, apply to the sequence string and return a string or a list
        of one-letter codes.
        If `func` is an iterable of functions, use the corresponding composite
        function e.g. if func == [f, g]: func = lambda x: g(f(x)).

    Yields
    ------
    (identifier, seq) : tuple (str, str)
        For each record, a tuple containing identifier and sequence.

    """
    from collections import Iterable
    from lilbio.bioparsers import bioparsers
    from lilbio.funcs import compose

    try:
        bioparser = bioparsers[fmt]
    except KeyError:
        raise UnsupportedFormatError(fmt)

    if func is None:

        def func(x):  # pylint: disable=function-redefined
            return x

    if isinstance(func, Iterable):
        func = compose(*func)

    if not callable(func):
        raise NotCallableError(func)

    data = gopen.gread(source)
    parsed_data = bioparser(data)
    for title, seq in parsed_data:
        yield title, func(seq)


def write(a, f=sys.stdout):
    """Write as FASTA file."""
    tostr = lilbio.funcs.tostr
    for r in a:
        string_record = '>%s\n%s' % (r[0], tostr(r[1]))
        print(string_record, file=f)


def main():
    """main."""
    import argparse
    parser_ = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser_.add_argument('-i', '--infile', type=str, help='Input file name')
    parser_.add_argument('-f',
                         '--format',
                         type=str,
                         help='Input format',
                         default='fasta')
    args = parser_.parse_args()
    filename = args.infile
    fmt = args.format

    parsed_records = parse(filename, fmt)
    for identifier, seq in parsed_records:
        print('>%s\n%s' % (identifier, seq))


if __name__ == '__main__':
    main()
