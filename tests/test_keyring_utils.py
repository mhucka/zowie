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
from zowie.keyring_utils import keyring_credentials, save_keyring_credentials

def test_encoding():
    assert _decoded(_encoded('abc', '123')) == ('abc', '123')

def test_keyring():
    save_keyring_credentials('@@testingkey@@', '@@testingid@@', '@@testring@@')
    assert keyring_credentials('@@testring@@') == ('@@testingkey@@', '@@testingid@@')
