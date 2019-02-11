# -*- coding: utf-8 -*-
# Author: Simone Marsili <simomarsili@gmail.com>
# License: BSD 3 clause
"""alignment parser"""
import sys
import logging
import gopen

logger = logging.getLogger(__name__)


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
        When passed, apply to the sequence string.
        If `func` is an iterable of functions, use the corresponding composite
        function e.g. if func == [f, g]: func = lambda x: g(f(x)).

    Yields
    ------
    (header, seq) : tuple (str, str)
        For each record, a tuple containing header and sequence.

    """
    from collections import Iterable
    from lilbio.bioparsers import bioparsers
    from lilbio.funcs import compose

    try:
        bioparser = bioparsers[fmt]
    except KeyError:
        raise ValueError('%s format is not supported' % fmt)

    if not func:

        def func(x):
            return x

    if isinstance(func, Iterable):
        func = compose(*func)

    if not callable(func):
        raise TypeError('%s object is not callable' % type(func))

    data = gopen.gread(source)
    parsed_data = bioparser(data)
    for title, seq in parsed_data:
        yield title, func(seq)


def write(a, f=sys.stdout):
    for r in a:
        string_record = '>%s\n%s' % (r[1], r[2])
        print(string_record, file=f)


def main():
    import argparse
    parser_ = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser_.add_argument('-i', '--infile', type=str, help='Input file name')
    parser_.add_argument(
        '-f', '--format', type=str, help='Input format', default='fasta')
    args = parser_.parse_args()
    filename = args.infile
    fmt = args.format

    parsed_records = parse(filename, fmt)
    for title, seq in parsed_records:
        print('%s\n%s' % (title, seq))


if __name__ == '__main__':
    main()
