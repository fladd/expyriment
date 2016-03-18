"""The misc package.

This package contains miscellaneous classes, modules and functions.

See also expyriment.misc.extras for more misc.

"""
from __future__ import absolute_import

__author__ = 'Florian Krause <florian@expyriment.org> \
              Oliver Lindemann <oliver@expyriment.org>'
__version__ = ''
__revision__ = ''
__date__ = ''


from . import defaults
from ._miscellaneous import compare_codes, add_fonts, list_fonts, find_font
from ._miscellaneous import unicode2byte, byte2unicode, numpad_digit_code2ascii
from ._miscellaneous import get_monitor_resolution
from . import constants
from ._buffer import  Buffer, ByteBuffer
from ._clock import Clock
from ._hsv_colour import HSVColour
from . import geometry
from . import data_preprocessing
from . import statistics
