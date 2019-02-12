# -*- coding: utf-8 -*-
# Author: Simone Marsili <simomarsili@gmail.com>
# License: BSD 3 clause
"""Utility functions."""

import logging
import functools

__all__ = [
    'is_command',
]


def is_command(cmds):
    """Given one command returns its path, or None.
    Given a list of commands returns the first recoverable path, or None.
    """
    try:
        from shutil import which as which  # python3 only
    except ImportError:
        from distutils.spawn import find_executable as which

    if isinstance(cmds, str):
        return which(cmds)
    else:
        for cmd in cmds:
            path = which(cmd)
            if path is not None:
                return path
        return path


def open_tempfile():
    import tempfile
    tempfile = tempfile.NamedTemporaryFile
    kwargs = {'delete': True, 'mode': 'r+'}
    return tempfile(**kwargs)


def timeit(func):
    """Timeit decorator."""

    @functools.wraps(func)
    def timed(*args, **kwargs):
        import time
        ts0 = time.time()
        result = func(*args, **kwargs)
        ts1 = time.time()
        logging.debug('%r: %2.4f secs', func, ts1 - ts0)
        return result

    return timed


def config_loggers():
    # set log messages
    # add_loglevel_notes()
    logging.basicConfig(
        # filename=logname,
        # filemode='a',
        format='%(module)-10s %(funcName)-20s: %(levelname)-8s %(message)s',
        datefmt='%H:%M:%S',
        # level=logging.DEBUG)
        level=logging.WARNING)
    # add_notes_handler()
