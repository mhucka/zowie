'''
wherefrom.py: writes Zotero select link into the "Where from" metadata field

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
from   bun import inform, warn
from   commonpy.string_utils import antiformat
import re
from   xattr import getxattr, setxattr, listxattr

if __debug__:
    from sidetrack import log

from .base import WriterMethod


# Class definitions.
# .............................................................................

class WhereFrom(WriterMethod):
    '''Implements writing Zotero links into the "Where from" metadata field.'''

    @classmethod
    def name(self):
        return 'wherefrom'


    @classmethod
    def description(self):
        return ('Prepends the Zotero select link to the "Where from" metadata'
                + ' field of a file, which is typically used by macOS to store'
                + " a file's download origin. If macOS Spotlight indexing is"
                + ' turned on for the volume containing the file, the macOS'
                + ' Finder will display the upated "Where from" value(s) in'
                + ' the Get Info panel of the file; if Spotlight is not turned'
                + ' on, the Get info panel will not be updated, but commands'
                + ' such as xattr will correctly show changes to the value.'
                + ' This metadata field can be a list; thus, it is possible'
                + ' to add a value without losing previous values.')

    def write_link(self, file, uri, dry_run, overwrite):
        '''Write the "uri" into the "Where From" metadata attribute of "file".'''

        path = antiformat(f'[grey89]{file}[/]')
        if not overwrite:
            if __debug__: log(f'reading extended attributes of {file}')
            if b'com.apple.metadata:kMDItemWhereFroms' in listxattr(file):
                wherefroms = getxattr(file, b'com.apple.metadata:kMDItemWhereFroms')
                wherefroms = biplist.readPlistFromString(wherefroms)
                if __debug__: log(f'read wherefroms value {wherefroms} on {file}')
                if type(wherefroms) == str:
                    if __debug__: log(f'wherefroms value is a string on {file}')
                    # Has to be a list for DEVONthink to parse it, so reformat it.
                    if wherefroms == uri:
                        inform(f'Reformating already-present link in "Where from" of {path}')
                        wherefroms = [uri]
                    else:
                        inform(f'Adding Zotero link to front of "Where from" of {path}')
                        wherefroms = [uri,  wherefroms]
                elif wherefroms[0] == uri:
                    inform(f'Zotero link already present in "Where from" of {path}')
                    return
                elif type(wherefroms[0]) is str and wherefroms[0].startswith('zotero://'):
                    warn(f'Replacing existing Zotero link in "Where from" of {path}')
                    wherefroms[0] = uri
                else:
                    inform(f'Adding Zotero link to front of "Where from" of {path}')
                    wherefroms.insert(0, uri)
            else:
                if __debug__: log(f'no prior wherefroms found on {file}')
                inform(f'Writing Zotero link into "Where From" metadata of {path}')
                wherefroms = [uri]
        else:
            inform(f'Overwriting "Where From" metadata with Zotero link in {path}')
            wherefroms = [uri]

        binary = biplist.writePlistToString(wherefroms)
        if __debug__: log(f'writing "where froms" extended attribute of {file}')
        setxattr(file, b'com.apple.metadata:kMDItemWhereFroms', binary)