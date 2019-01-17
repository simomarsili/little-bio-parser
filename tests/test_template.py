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
    import gopen
    from lilp.bioparsers import fasta_parser
    fname = os.path.join(tests_dir(), '1.fa')
    lines = gopen.read(fname)
    a = list(fasta_parser(lines))
    assert repr(a) == "[('1', '-AAA'), ('2', 'B-BB'), ('3', 'CC-C'), ('4', 'DDD-')]"
