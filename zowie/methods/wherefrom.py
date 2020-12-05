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
        return ('Writes the Zotero select link to the "Where from" metadata'
                + ' field of each file (the com.apple.metadata:kMDItemWhereFroms'
                + ' extended attribute). This field is displayed as "Where from"'
                + ' in Finder "Get Info" panels; it is typically used by web'
                + ' browsers to store a files download origin. The field is a'
                + ' list. If Zowie finds a Zotero select link as the first item'
                + ' in the list, it updates its value; otherwise, Zowie prepends'
                + ' the Zotero select link to the list of existing values,'
                + ' keeping the other values unless the overwrite option (-o) is'
                + ' used. When the overwrite option is used, Zowie deletes the'
                + ' existing list of values and writes only the Zotero select'
                + ' link. Note that if macOS Spotlight indexing is turned on for'
                + ' the volume containing the file, the macOS Finder will'
                + ' display the upated "Where from" values in the Get Info panel'
                + ' of the file; if Spotlight is not turned on, the Get info'
                + ' panel will not be updated, but other applications will'
                + ' still be able to read the updated value.')


    def write_link(self, file, uri):
        '''Write the "uri" into the "Where From" metadata attribute of "file".'''

        path = antiformat(f'[grey89]{file}[/]')
        if not self.overwrite:
            wherefroms = self._wherefroms(file)
            if wherefroms:
                if wherefroms[0] == uri:
                    inform(f'Zotero link already present in "Where from" of {path}')
                    return
                elif type(wherefroms[0]) is str and wherefroms[0].startswith('zotero://'):
                    inform(f'Updating existing Zotero link in "Where from" of {path}')
                    wherefroms[0] = uri
                else:
                    inform(f'Prepending Zotero link to front of "Where from" of {path}')
                    wherefroms.insert(0, uri)
            else:
                if __debug__: log(f'no prior wherefroms found on {file}')
                inform(f'Writing Zotero link into "Where From" metadata of {path}')
                wherefroms = [uri]
        else:
            inform(f'Overwriting "Where From" metadata with Zotero link in {path}')
            wherefroms = [uri]

        self._write_wherefroms(file, wherefroms)


    def _wherefroms(self, file):
        if b'com.apple.metadata:kMDItemWhereFroms' in listxattr(file):
            wherefroms = getxattr(file, b'com.apple.metadata:kMDItemWhereFroms')
            wherefroms = biplist.readPlistFromString(wherefroms)
            if __debug__: log(f'found wherefroms value {wherefroms} on {file}')
            # The value should be an array of strings. If it's a string alone,
            # then something else wrote it incorrectly. DEVONthink will not
            # read it unless it's an array. We could correct the format, even
            # if ultimately we don't write a new value, but if we end up not
            # writing a different value, does that still count as modifying the
            # file metadata? I don't know. Let's decide based on overwrite.
            if type(wherefroms) == str:
                if __debug__: log(f'wherefroms is a string on {file}')
                wherefroms = [uri]
                if self.overwrite:
                    if __debug__: log(f'rewriting string wherefroms on {file}')
                    self._write_wherefroms(file, wherefroms)
            return wherefroms
        else:
            if __debug__: log(f'no kMDItemWhereFroms attribute on {file}')
            return None


    def _write_wherefroms(self, file, wherefroms):
        binary = biplist.writePlistToString(wherefroms)
        if __debug__: log(f'writing "where froms" extended attribute of {file}')
        setxattr(file, b'com.apple.metadata:kMDItemWhereFroms', binary)
