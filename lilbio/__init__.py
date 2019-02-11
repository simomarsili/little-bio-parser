# -*- coding: utf-8 -*-
# Author: Simone Marsili <simomarsili@gmail.com>
# License: BSD 3 clause
"""A little parser for alignments of biological sequences."""

import time
import logging
import pkg_resources
from lilbio.utils import config_loggers
from lilbio.parser import parse, write
import lilbio.funcs

project_name = 'little-bio-parser'
__version__ = pkg_resources.require(project_name)[0].version
__copyright__ = 'Copyright (C) 2017 Simone Marsili'
__license__ = 'BSD 3 clause'
__author__ = 'Simone Marsili (simo.marsili@gmail.com)'
__all__ = ['parse', 'write']

config_loggers()
logger = logging.getLogger(__name__)
now = time.strftime('%Y-%m-%d %H:%M:%S')
header = ('lilp (%s) - %s' % (__version__, now))
logger.info(header)
logger.info('=' * len(header))
