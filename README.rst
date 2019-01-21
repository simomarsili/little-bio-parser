=================
little-bio-parser
=================
A minimalistic parser for sequence alignments
(fasta or stockholm formats).

The parser returns an iterator over the alignment records as
(index, title, sequence) tuples.

Usage example::

  >>> import lilbio
  >>> parsed_records = lilbio.parse('alignment.fa', 'fasta')

No record objects are created. No check on biological alphabet.

Built over modified low-level parsers from Biopython
(SimpleFastaParser function and StockholmIterator class).
