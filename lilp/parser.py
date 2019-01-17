"""alignment parser"""
import logging
from itertools import islice
import lilp.alphabets
import gopen

logger = logging.getLogger(__name__)


def parse(source, hmm=False, alphabet=None):
    from lilp.bioparsers import bioparsers

    # guess alignment format
    fmt, bioparser = _guess_parser(source, bioparsers)

    # get sample of 20 sequences
    sample = [rec[1] for rec in islice(bioparser(source), 20)]

    # list of HMM positions
    selection = [p for p, c in enumerate(sample[0])
                 if c in lilp.alphabets.GENERIC_ALPHABET]

    np0 = len(sample[0])  # #positions
    np1 = len(selection)  # #HMM positions
    if np1 == np0:
        selection = None
    else:
        if hmm:
            logging.info('Removed %s "insertion" positions (%s/%s left)',
                         np0 - np1, np1, np0)
        else:
            logging.info('Lowercase/dot converted to uppercase/gap.')

    if not alphabet:
        alphabet = lilp.alphabets.alphabet_guess(sample)

    if alphabet not in lilp.alphabets.ALPHABETS:
        logging.error(
            '''
            %s is not a valid alphabet (see skmmsa.alphabets.ALPHABETS).
            Will guess a valid alphabet.
            ''', alphabet)
        alphabet = lilp.alphabets.alphabet_guess(sample)

    # alignment data
    data = {'n0': 0,               # total n. of sequences
            'n1': 0,               # sequences compliant with alphabet
            'fmt': fmt,            # alignment format
            'alphabet': alphabet}  # alignment alphabet

    def parsed():
        for name, seq in bioparser(source):
            data['n0'] += 1
            if selection:
                if hmm:
                    # filter HMM positions
                    seq = ''.join([seq[p] for p in selection])
                else:
                    # convert lowercase/dot symbols to uppercase/gap.
                    seq = seq.upper().replace('.', '-')
            if set(seq) <= set(alphabet):
                data['n1'] += 1
                yield data['n0'] - 1, name, seq

    return parsed(), data


def _guess_parser(source, parsers):
    """Guess MSA format.

    Parameters
    ----------
    source : file

    parsers : dict
        map format to parser generator function

    Returns
    -------
    (format, parser) : tuple
        Format and relevant parser.

    """

    logger.info('Guess alignment format.')

    alignment_parser = None
    for fmt, parser in parsers.items():
        try:
            # parser is a generator function
            next(parser(source))
            alignment_parser = parser
            alignment_format = fmt
            logger.debug('Test %r format.', alignment_format)
            source.seek(0)
            break
        except (StopIteration, ValueError):
            continue

        if alignment_parser is not None:
            logger.info('Alignment format guess: %r', alignment_format)
            break
    else:
        raise ValueError('Cant recognize alignment format. '
                         'Valid formats are: FASTA, Stockholm')

    return (alignment_format, alignment_parser)


def main():
    import sys
    import argparse
    parser_ = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter, epilog=" ")
    parser_.add_argument(
        '-i', '--infile', type=argparse.FileType('r'), help='Input file name',
        default=sys.stdin)
    parser_.add_argument(
        '-f', '--format', type=str, help='Input format', default='fasta')
    args = parser_.parse_args()
    filename = args.infile
    fmt = args.format

    next(parse(filename))


if __name__ == '__main__':
    main()
