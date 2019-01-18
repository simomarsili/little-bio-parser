=================
little-bio-parser
=================
Minimal parser for files of biological alignments.
Valid formats are: "fasta" and "stockholm".

The parser simply iterates over the alignment returning each record as a tuple
(index, title, seq):
- the index in the original alignment
- the title line
- and the sequence (as a plain string)
No record objects are created. No check on biological alphabet.

Built over low level parsers from Biopython
(SimpleFastaParser function and StockholmIterator class).
