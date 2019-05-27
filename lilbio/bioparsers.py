# -*- coding: utf-8 -*-
# Copyright 2006-2015 by Peter Cock.  All rights reserved.
# Revisions copyright 2015 by Ben Woodcroft.  All rights reserved.
# Modifications copyright 2016 by Simone Marsili.
#
# Biopython License Agreement
# ---------------------------
#
# Permission to use, copy, modify, and distribute this software and its
# documentation with or without modifications and for any purpose and
# without fee is hereby granted, provided that any copyright notices
# appear in all copies and that both those copyright notices and this
# permission notice appear in supporting documentation, and that the
# names of the contributors or copyright holders not be used in
# advertising or publicity pertaining to distribution of the software
# without specific prior permission.

# THE CONTRIBUTORS AND COPYRIGHT HOLDERS OF THIS SOFTWARE DISCLAIM ALL
# WARRANTIES WITH REGARD TO THIS SOFTWARE, INCLUDING ALL IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS, IN NO EVENT SHALL THE
# CONTRIBUTORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY SPECIAL, INDIRECT
# OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS
# OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE
# OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE
# OR PERFORMANCE OF THIS SOFTWARE.
"""(Decorated) Biopython parsers."""
import logging

logger = logging.getLogger(__name__)
__all__ = [
    'bioparsers',
    'fasta_parser',
    'stockholm_parser',
]

bioparsers = {}


def bioparser(parsers, fmt=None):
    """Register the format of the decorated parser generator function.
    """

    def decorator(parser_func):
        import inspect
        try:
            assert inspect.isgeneratorfunction(parser_func)
        except AssertionError:
            raise TypeError('%r is not a valid parser generator function')
        if fmt:
            fmt1 = str(fmt)
        else:
            fmt1 = parser_func.__name__

        def decorated_parser(source):
            """Handle iterables, file-like and compressed files."""
            import collections
            import gopen
            if isinstance(source, collections.Iterable):
                for name, seq in parser_func(source):
                    yield name, seq
            else:
                with gopen.readable(source) as f:
                    for name, seq in parser_func(f):
                        yield name, seq

        parsers[fmt1] = decorated_parser

        return decorated_parser

    return decorator


@bioparser(bioparsers, 'fasta')
def fasta_parser(fileo):
    """Generator of Fasta records.
    Adapted from Biopython SimpleFastaParser.
    (https://raw.githubusercontent.com/biopython/biopython/biopython-168/Bio/SeqIO/FastaIO.py)

    For each record a tuple of two strings is returned, the FASTA title
    line (without the leading '>' character), and the sequence (with any
    whitespace removed). The title line is not divided up into an
    identifier (the first word) and comment or description.

    Parameters
    ----------
    fileo : file object

    Returns
    -------
    (seqname, sequence) : (str, str)
        Next record in the alignment as tuple (seqname, sequence)

    """
    # Skip any text before the first record (e.g. blank lines, comments)
    # TODO: add a maximum number of lines for the initial comment

    # make sure that fileo is an iterator
    fileo = iter(fileo)
    # skip blank lines (only) till a record is found
    while True:
        line = next(fileo, None)
        if not line:
            return  # Premature end of file, or just empty?
        if line[0] == '>':
            break
        elif line[0] != ';':
            raise ValueError('Not Fasta format')

    while True:
        if line[0] != '>':
            raise ValueError(
                'Records in Fasta files should start with ">" character')
        title = line[1:].rstrip()
        lines = []
        line = next(fileo, None)
        while line:
            if line[0] == '>':
                break
            lines.append(line.rstrip())
            line = next(fileo, None)

        # Remove trailing whitespace, and any internal spaces
        # (and any embedded \r which are possible in mangled files
        # when not opened in universal read lines mode)
        yield (title, ''.join(lines).replace(' ', '').replace('\r', ''))

        if not line:
            return  # StopIteration

    assert False, 'Should not reach this line'


@bioparser(bioparsers, 'stockholm')
def stockholm_parser(fileo):
    """Generator of Stockholm records.
    Adapted from Biopyhon StockholmIterator.
    (https://raw.githubusercontent.com/biopython/biopython/biopython-168/Bio/AlignIO/StockholmIO.py)

    Parameters
    ----------
    fileo : file object

    Returns
    -------
    (seqname, sequence) : (str, str)
        Next record in the alignment as tuple (seqname, sequence)

    """

    # make sure that fileo is an iterator
    fileo = iter(fileo)
    while True:
        line = next(fileo, None)
        if not line:
            break  # end of file
        line = line.strip()  # remove trailing \n
        if line == '//':
            return  # end of alignment
        if line == '':
            # blank line, ignore
            pass
        elif line[0] != '#':
            if line[0] in ['>', ';']:
                raise ValueError('Not Stockholm format')
            # Sequence
            # Format: '<seqname> <sequence>'
            parts = [x.strip() for x in line.split(' ', 1)]
            if len(parts) != 2:
                # This might be someone attempting to store
                # a zero length sequence?
                raise ValueError('Could not split line into identifier '
                                 'and sequence:\n' + line)
            title, seq = parts
            # do not replace dots with gaps!
            # seqs[id] += seq.replace(".", "-")
            yield (title, seq)

    assert False, 'Should not reach this line'
