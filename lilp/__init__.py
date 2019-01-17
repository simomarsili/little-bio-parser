# -*- coding: utf-8 -*-
# Copyright (C) 2019, Simone Marsili
# All rights reserved.
# License: BSD 3 clause
# Author: Simone Marsili (simomarsili@gmail.com)
"""A little parser for alignments of biological sequences."""

import time
import logging
from lilp.utils import get_version, config_loggers


__version__ = get_version()
__copyright__ = 'Copyright (C) 2017 Simone Marsili'
__license__ = 'BSD 3 clause'
__author__ = 'Simone Marsili (simo.marsili@gmail.com)'


config_loggers()
logger = logging.getLogger(__name__)
now = time.strftime('%Y-%m-%d %H:%M:%S')
header = ('lilp (%s) - %s' % (__version__, now))
logger.info(header)
logger.info('=' * len(header))
