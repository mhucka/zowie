'''
findercomment.py: write Zotero select link into a file's macOS Finder comments

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
from   bun import inform, warn
from   commonpy.string_utils import antiformat
import re

from .base import WriterMethod

if __debug__:
    from sidetrack import log


# Constants.
# .............................................................................

# The following code is based in part on code from Python package "osxmetadata"
# version 0.99.10 of 2020-09-01, Copyright (c) 2020 Rhet Turnbull.
# https://github.com/RhetTbull/osxmetadata/blob/master/osxmetadata/findercomments.py

_FINDER_SCRIPTS = applescript.AppleScript('''
on get_comments{f}
    tell application "Finder"
        return comment of (POSIX file f as alias)
    end tell
end run

on set_comments{f, c}
    tell application "Finder"
        set comment of (POSIX file f as alias) to c
    end tell
end run

on clear_comments{f}
    tell application "Finder"
        set c to missing value
        set comment of (POSIX file f as alias) to c
    end tell
end run
''')


# Class definitions.
# .............................................................................

class FinderComment(WriterMethod):
    '''Implements writing Zotero URI into the macOS Finder comments for a file.'''

    @classmethod
    def name(cls):
        return 'findercomment'


    @classmethod
    def description(cls):
        return ('(Default method.)'
                + ' Writes the Zotero select link into the Finder comments of'
                + ' each file, attempting to preserve other parts of the'
                + ' comments. If Zowie finds an existing Zotero select link in'
                + ' the text of the Finder comments attribute, it only updates'
                + ' the link portion and tries to leave the rest of the'
                + ' comment text untouched. Otherwise, Zowie ONLY writes'
                + ' into the comments attribute if either the attribute value is'
                + ' empty or Zowie is given the overwrite (-o) option. (Note'
                + ' that updating the link text requires rewriting the entire'
                + ' Finder comments attribute on a given file. Finder comments'
                + ' have a reputation for being easy to get into inconsistent'
                + ' states, so if you have existing Finder comments that you'
                + " absolutely don't want to lose, it may be safest to avoid"
                + ' this method.)')


    @classmethod
    def file_extension(cls):
        '''Returns the file extension to which this method is limited
        A value of None means it is not limited to any particular file type.
        '''
        return None


    def write_link(self, file_path, uri):
        '''Writes the "uri" into the Finder comments of file "file_path".

        If there's an existing comment, read it.  If there's a Zotero select
        link as the first thing in the comment, replace that URI with this one,
        under the assumption that this was a link written by a prior run of
        this program; otherwise, prepend the Zotero select link to the finder
        comments.  In either case, write the results back.
        '''

        # file pathname string may contain '{' and '}', so guard against it.
        fp = antiformat(file_path)
        file = antiformat(f'[steel_blue3]{file_path}[/]')
        if not self.overwrite:
            if __debug__: log(f'reading Finder comments of {fp}')
            comments = _FINDER_SCRIPTS.call('get_comments', file_path)
            if comments and uri in comments:
                inform(f'Zotero link already present in Finder comments of {file}')
                return
            elif comments and 'zotero://select' in comments:
                inform(f'Replacing existing Zotero link in Finder comments of {file}')
                if __debug__: log(f'overwriting existing Zotero link with {uri}')
                comments = re.sub(r'(zotero://\S+)', uri, comments)
            elif comments:
                warn(f'Not overwriting existing Finder comments of {file}')
                return
            else:
                inform(f'Writing Zotero link into empty Finder comments of {file}')
                comments = uri
        else:
            inform(f'Ovewriting Finder comments with Zotero link for {file}')
            comments = uri

        if not self.dry_run:
            if __debug__: log(f'invoking AS function to clear comment on {fp}')
            _FINDER_SCRIPTS.call('clear_comments', file_path)
            if __debug__: log(f'invoking AS function to set comment on {fp}')
            _FINDER_SCRIPTS.call('set_comments', file_path, comments)
