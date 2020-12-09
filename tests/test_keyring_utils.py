import os
import pytest
import sys
from   time import time

try:
    thisdir = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(os.path.join(thisdir, '..'))
except:
    sys.path.append('..')

from zowie.keyring_utils import _encoded, _decoded

def test_encoding():
    assert _decoded(_encoded('abc', '123')) == ('abc', '123')
