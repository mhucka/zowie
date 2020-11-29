'''
wherefrom.py: write Zotero URI into the "Where from" metadata field

Authors
-------

Michael Hucka <mhucka@caltech.edu> -- Caltech Library

Copyright
---------

Copyright (c) 2020 by Michael Hucka and the California Institute of Technology.
This code is open-source software released under a 3-clause BSD license.
Please see the file "LICENSE" for more information.
'''

import applescript
import biplist
from   bun import inform
from   commonpy.string_utils import antiformat
import re
from   xattr import getxattr, setxattr, listxattr

if __debug__:
    from sidetrack import log

from .base import WriterMethod


# Class definitions.
# .............................................................................

class WhereFrom(WriterMethod):
    def name(self):
        return 'wherefrom'


    def description(self):
        return ('Prepends the Zotero item URI to the "Where from" metadata field'
                + ' of a file, which is typically used by macOS to store a'
                + " file's download origin. DEVONthink sets the docoument"
                + ' "URL" property value from this field upon file import and'
                + ' export. If macOS Spotlight indexing is turned on for the'
                + ' volume containing the file, the macOS Finder will display'
                + ' the upated "Where from" values in the Get Info panel of the'
                + ' file; if Spotlight is not turned on, the Get info panel'
                + ' will not be updated, but commands such as xattr will'
                + ' correctly show changes to the value. This metadata field'
                + ' is a list; thus, that it is possible to add a value without'
                + ' losing previous values. However, DEVONthink only uses the'
                + ' first value, and most other applications do not even'
                + ' provide a way to view the value(s).')


    def write_uri(self, file, uri, dry_run):
        '''Write the "uri" into the "Where From" metadata attribute of "file".'''

        path = antiformat(f'[grey89]{file}[/]')
        if __debug__: log(f'reading extended attributes of {file}')
        if 'com.apple.metadata:kMDItemWhereFroms' in listxattr(file):
            wherefroms = getxattr(file, 'com.apple.metadata:kMDItemWhereFroms')
            wherefroms = biplist.readPlistFromString(wherefroms)
            if __debug__: log(f'found {len(wherefroms)} wherefroms on {file}')
            if wherefroms[0] == uri:
                inform(f'Zotero URI already present in "Where from" of {path}')
                return
            elif 'zotero://select' in wherefroms[0]:
                inform(f'Replacing existing Zotero URI in "Where from" of {path}')
                wherefroms[0] = uri
            else:
                import pdb; pdb.set_trace()
                wherefroms.insert(0, uri)
        else:
            if __debug__: log(f'no prior wherefroms found on {file}')
            inform(f'Writing Zotero URI into "Where From" metadata of file {path}')
            wherefroms = [uri]

        binary = biplist.writePlistToString(wherefroms)
        setxattr(file, 'com.apple.metadata:kMDItemWhereFroms', binary)
