def tests_dir():
    """Return None is no tests dir."""
    import os
    cwd = os.getcwd()
    basename = os.path.basename(cwd)
    if basename == 'tests':
        return cwd
    else:
        tests_dir = os.path.join(cwd, 'tests')
        if os.path.exists(tests_dir):
            return tests_dir


def test_0():
    assert 1 == 1


def test_fasta():
    import os
    from gopen import gread
    from lilp.bioparsers import fasta_parser
    fname = os.path.join(tests_dir(), '1.fa')
    a = [record for record in fasta_parser(gread(fname))]
    assert repr(a) == "[('1', '-AAA'), ('2', 'B-BB'), ('3', 'CC-C'), ('4', 'DDD-')]"
