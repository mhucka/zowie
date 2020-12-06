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

from .base import WriterMethod
from ..exceptions import FileError

if __debug__:
    from sidetrack import log


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

        # file pathname string may contain '{' and '}', so guard against it.
        fp = antiformat(file)
        path = antiformat(f'[steel_blue3]{file}[/]')
        if not self.overwrite:
            (wherefroms, malformed) = self._wherefroms(file)
            if wherefroms:
                if wherefroms[0] == uri:
                    inform(f'Zotero link already present in "Where from" of {path}')
                    # We found a link already present, but the attribute value
                    # was malformed (maybe due to the use of a buggy previous
                    # version of Zowie or manual experiments by the user). We
                    # should proceed to correct it even if -o is not in effect.
                    if not malformed:
                        return
                elif type(wherefroms[0]) is str and wherefroms[0].startswith('zotero://'):
                    inform(f'Updating existing Zotero link in "Where from" of {path}')
                    wherefroms[0] = uri
                else:
                    inform(f'Prepending Zotero link to front of "Where from" of {path}')
                    wherefroms.insert(0, uri)
            else:
                if __debug__: log(f'no prior wherefroms found on {fp}')
                inform(f'Writing Zotero link into "Where From" metadata of {path}')
                wherefroms = [uri]
        else:
            inform(f'Overwriting "Where From" metadata with Zotero link in {path}')
            wherefroms = [uri]

        self._write_wherefroms(file, wherefroms)


    def _wherefroms(self, file):
        '''Returns a tuple (wherefroms, malformed), where the second element
        indicates where the content was malformed in some way.'''

        fp = antiformat(file)
        if b'com.apple.metadata:kMDItemWhereFroms' in listxattr(file):
            wherefroms = getxattr(file, b'com.apple.metadata:kMDItemWhereFroms')
            if not wherefroms.startswith(b'bplist'):
                # There's content, but it's not a list. We don't know how to
                # parse it and can't anticipate every possible variation, but
                # we shouldn't leave it or destroy it either, if we can help it.
                if __debug__: log(f'wherefroms {wherefroms} is not a list on {fp}')
                try:
                    # We want to return an array of strings. Here, we have
                    # bytes. Try to convert it, just in case we succeed.
                    wherefroms = wherefroms.decode()
                except UnicodeDecodeError:
                    raise FileError('Malformed non-list value for attribute'
                                    + ' com.apple.metadata:kMDItemWhereFroms'
                                    + f' on file {fp}')
                return ([wherefroms], True)
            try:
                wherefroms = biplist.readPlistFromString(wherefroms)
            except biplist.InvalidPlistException as ex:
                if __debug__: log(f'got exception {str(ex)} parsing wherefroms of {fp}')
                # The property exists, it looks like a list, but it failed to
                # parse. We can't treat it as preexisting content because it'll
                # probably screw up something else. If we're going to overwrite
                # it anyway, we won't get to this point anyway. Otherwise:
                raise FileError('Unable to parse attribute'
                                + ' com.apple.metadata:kMDItemWhereFroms'
                                + f' on file {fp}')
            return (wherefroms, False)
        else:
            if __debug__: log(f'no kMDItemWhereFroms attribute on {fp}')
            return (None, False)


    def _write_wherefroms(self, file, wherefroms):
        binary = biplist.writePlistToString(wherefroms)
        if __debug__: log(f'writing "where froms" attribute of {antiformat(file)}')
        setxattr(file, b'com.apple.metadata:kMDItemWhereFroms', binary)
