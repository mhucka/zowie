# -*- mode: python -*-
# =============================================================================
# @file    pyinstaller-darwin.spec
# @brief   Spec file for PyInstaller for macOS
# @author  Michael Hucka
# @license Please see the file named LICENSE in the project directory
# @website https://github.com/mhucka/zowie
# =============================================================================

import imp
import os
from   PyInstaller.utils.hooks import copy_metadata
import sys

# The data_files setting below following fixes this run-time error:
#
#   File "humanize/__init__.py", line 14, in <module>
#   File "pkg_resources/__init__.py", line 465, in get_distribution
#   File "pkg_resources/__init__.py", line 341, in get_provider
#   File "pkg_resources/__init__.py", line 884, in require
#   File "pkg_resources/__init__.py", line 770, in resolve
#   pkg_resources.DistributionNotFound: The 'humanize' distribution was
#   not found and is required by the application
#
# I don't actually know why that error occurs.  CommonPy imports humanize,
# and it has it in its requirements.txt, and PyInstaller looks like it's
# picking it up.  So I'm stumped about why humanize seems to get missed in
# the binary produced by PyInstaller.  Don't have time to debug more.
data_files = copy_metadata('humanize')

configuration = Analysis(['zowie/__main__.py'],
                         pathex = ['.'],
                         binaries = [],
                         datas = data_files,
                         hiddenimports = ['keyring.backends',
                                          'keyring.backends.OS_X'],
                         hookspath = [],
                         runtime_hooks = [],
                         # For reasons I can't figure out, PyInstaller tries
                         # to load these even though they're never imported
                         # by the Zowie code.  Have to exclude them manually.
                         excludes = ['PyQt4', 'PyQt5', 'gtk', 'matplotlib',
                                     'numpy'],
                         win_no_prefer_redirects = False,
                         win_private_assemblies = False,
                         cipher = None,
                        )

application_pyz    = PYZ(configuration.pure,
                         configuration.zipped_data,
                         cipher = None,
                        )

executable         = EXE(application_pyz,
                         configuration.scripts,
                         configuration.binaries,
                         configuration.zipfiles,
                         configuration.datas,
                         name = 'zowie',
                         debug = False,
                         strip = True,
                         upx = False,
                         runtime_tmpdir = None,
                         console = False,
                        )
