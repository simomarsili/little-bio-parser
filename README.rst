=================
little-bio-parser
=================
Minimal parser for files of biological alignments (fasta or stockholm formats).

The parser returns a generator of the alignment records as
(index, title, sequence) tuples, where:

- index is the index in the original alignment
- title is the header line
- and sequence is the record sequence (as a plain string)

Usage example::

  >>> import lilbio
  >>> parsed_records = lilbio.parse('alignment.fa', 'fasta')

No record objects are created. No check on biological alphabet.

Built over modified low-level parsers from Biopython
(SimpleFastaParser function and StockholmIterator class).
