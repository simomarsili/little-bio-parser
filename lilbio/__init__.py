# -*- coding: utf-8 -*-
# Author: Simone Marsili <simomarsili@gmail.com>
# License: BSD 3 clause
"""A little parser for alignments of biological sequences."""

import pkg_resources

from lilbio.funcs import uppercase_only
from lilbio.parser import parse, write

project_name = 'little-bio-parser'
__version__ = pkg_resources.require(project_name)[0].version
__copyright__ = 'Copyright (C) 2017 Simone Marsili'
__license__ = 'BSD 3 clause'
__author__ = 'Simone Marsili (simo.marsili@gmail.com)'
__all__ = ['parse', 'write', 'uppercase_only']
