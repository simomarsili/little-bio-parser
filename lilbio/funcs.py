"""Utils to operate on single records."""
import functools

GENERIC_ALPHABET = set('*-ABCDEFGHIJKLMNOPQRSTUVWXYZ')
UPPERCASE = {c.lower(): c for c in GENERIC_ALPHABET}
UPPERCASE['.'] = '-'


def compose(*funcs):
    """Compose a list of functions."""
    def fg(f, g):
        return lambda r: f(g(r))
    return functools.reduce(fg, funcs, lambda r: r)


def is_gappy(r, *, t=None):
    if t is None:
        raise ValueError('Specify a gap threshold in the range 0-1')
    seq = r[2]
    n = len(seq)
    ngaps = sum(1 for c in seq if c in {'-', '.'})
    if ngaps > t * n:
        return ngaps
    else:
        return False


def is_alphabet_consistent(r, *, alphabet=None):
    if alphabet is None:
        alphabet = set(GENERIC_ALPHABET)
    else:
        alphabet = set(alphabet)
    index, header, seq = r
    return all(c in alphabet for c in seq)


def uppercase(r):
    return map_symbols(r, m=UPPERCASE)


def filter_symbols(r, *, m=None):
    """
    Remove symbols not in `m`.

    If m is None, filter out symbols not in the generic alphabet:
    '*-ABCDEFGHIJKLMNOPQRSTUVWXYZ'

    Attributes
    ----------
    m : set

    Returns
    -------
    filtered record
    """
    return map_symbols(r, m=m)


def map_symbols(r, *, m=None):
    """
    m : dict or set
        If dict: map symbols from sequence.
        If symbol is not in `map`, leave it unchanged.
        If set: remove symbols not in `m`.
    """
    if m is None:
        m = set(GENERIC_ALPHABET)
    index, header, seq = r
    if isinstance(m, dict):
        seq = ''.join(m.get(c, c) for c in seq)  # map
    else:
        m = set(m)
        seq = ''.join(c for c in seq if c in m)  # filter
    return index, header, seq
