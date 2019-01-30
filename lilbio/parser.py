"""alignment parser"""
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
    func : callable
        When passed, apply to the sequence string.

    Yields
    ------
    (index, header, seq) : tuple (int, str, str)
        For each record, a tuple containing index, header and sequence.

    """

    from lilbio.bioparsers import bioparsers

    try:
        bioparser = bioparsers[fmt]
    except KeyError:
        raise ValueError('%s format is not supported' % fmt)

    if not func:
        def func(x):
            return x
    elif not callable(func):
        raise TypeError('%s object is not callable' % type(func))

    index = 0
    data = gopen.gread(source)
    parsed_data = bioparser(data)
    for title, seq in parsed_data:
        yield index, title, func(seq)
        index += 1


def main():
    import argparse
    parser_ = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser_.add_argument(
        '-i', '--infile', type=str, help='Input file name')
    parser_.add_argument(
        '-f', '--format', type=str, help='Input format', default='fasta')
    args = parser_.parse_args()
    filename = args.infile
    fmt = args.format

    parsed_records = parse(filename, fmt)
    for index, title, seq in parsed_records:
        print('%s %s\n%s' % (title, index, seq))


if __name__ == '__main__':
    main()
