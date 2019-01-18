"""alignment parser"""
import logging
import gopen

logger = logging.getLogger(__name__)


def parse(source, frmt):
    from lilbio.bioparsers import bioparsers

    try:
        bioparser = bioparsers[frmt]
    except KeyError:
        raise ValueError('%s format is not supported' % frmt)

    index = 0
    data = gopen.gread(source)
    parsed_data = bioparser(data)
    for title, seq in parsed_data:
        yield index, title, seq
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
