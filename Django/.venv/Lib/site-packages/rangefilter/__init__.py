# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import django

__author__ = "Daniel Lee"
__version__ = "0.9.1"

if django.VERSION < (3, 2):
    default_app_config = "rangefilter.apps.RangeFilterConfig"


VERSION = __version__
