'''
zotero_utils.py: utilities for interacting with Zotero libraries

Authors
-------

Michael Hucka <mhucka@caltech.edu> -- Caltech Library

Copyright
---------

Copyright (c) 2020 by Michael Hucka and the California Institute of Technology.
This code is open-source software released under a 3-clause BSD license.
Please see the file "LICENSE" for more information.
'''

from bun import inform, warn, alert, alert_fatal
from commonpy.interrupt import raise_for_interrupts
from commonpy.string_utils import antiformat
from collections import namedtuple
from os import path as path
from pyzotero import zotero, zotero_errors

from .exceptions import CannotProceed
from .exit_codes import ExitCode
from .keyring_utils import keyring_credentials, save_keyring_credentials
from .keyring_utils import validated_input

if __debug__:
    from sidetrack import log, logr


# Data definitions.
# .............................................................................

ZoteroRecord = namedtuple('ZoteroRecord', 'key parent_key file link record')
ZoteroRecord.__doc__ = '''Zotero data about a local file
  'key' is the Zotero key for the file attachment
  'parent_key' is the top-level record that contains the file attachment
  'file' is the path to the file on the local file system
  'link' is a Zotero select link of the form "zotero://select/..."
  'record' is the entire record from Zotero
'''


# Exported classes.
# .............................................................................

# maybe this should be a subclass of the pytoztero class?

class Zotero():
    '''Zotero interface class.'''

    def __init__(self, key, user_id, use_keyring):
        if key and (not key.isalnum() or len(key) < 20):
            alert_fatal(f'"{key}" does not appear to be a valid API key.')
            raise CannotProceed(ExitCode.bad_arg)
        if user_id and not user_id.isdigit():
            alert_fatal(f'"{user_id}" does not appear to be a Zotero user ID.')
            raise CannotProceed(ExitCode.bad_arg)

        # If the user supplied all the values on the command line, those are
        # the values used.  If none were supplied by the user on the command
        # line, all the values are retrieved from the user's keyring.  If
        # some were supplied and others missing, they're filled in from
        # either the keyring or by prompting the user.

        if __debug__: log('keyring {}', 'enabled' if use_keyring else 'disabled')
        if key is None and user_id is None and use_keyring:
            # We weren't given a key and id, but we can look in the keyring.
            if __debug__: log(f'getting id & key from keyring')
            key, user_id = keyring_credentials()
        if not key:
            key = validated_input('API key', key, lambda x: x.isalnum())
        if not user_id:
            user_id = validated_input('User ID', user_id, lambda x: x.isdigit())
        if use_keyring:
            if __debug__: log('saving credentials to keyring')
            save_keyring_credentials(key, user_id)

        self._key = key
        self._user_id = user_id

        # Get connected and store the Zotero conection object for the user
        # library first, then look up the group libraries that the user can
        # access and create Zotero objects for that too.  The way we use them,
        # we don't need to separate between them, so they all go into one list.

        self._libraries = []
        try:
            if __debug__: log(f'connecting to Zotero as user {user_id}')
            user = zotero.Zotero(user_id, 'user', key)
            # pyzotero will return an object but that doesn't mean the user
            # actually gave valid credentials. Need to try an operation.
            user.count_items()
            self._libraries.append(user)
            raise_for_interrupts()
        except zotero_errors.UserNotAuthorised as ex:
            if __debug__: log(f'got exception {str(ex)}')
            alert_fatal('Unable to connect to Zotero: invalid ID and/or API key.',
                        'The Zotero servers rejected attempts to connect.')
            raise CannotProceed(ExitCode.bad_arg)
        except KeyboardInterrupt as ex:
            if __debug__: log(f'got exception {str(ex)}')
            raise
        except Exception as ex:
            if __debug__: log(f'failed to create Zotero user object: str(ex)')
            alert_fatal('Unable to connect to Zotero API.')
            raise

        try:
            for group in user.groups():
                if __debug__: log(f'user can access group id {group["id"]}')
                self._libraries.append(zotero.Zotero(group['id'], 'group', key))
                raise_for_interrupts()
        except KeyboardInterrupt as ex:
            if __debug__: log(f'got exception {str(ex)}')
            raise
        except Exception as ex:
            if __debug__: log(f'failed to create Zotero group object: str(ex)')
            alert('Unable to retrieve Zotero group library; proceeding anyway.')


    def record_for_file(self, file):
        '''Returns a ZoteroRecord corresponding to the given local PDF file.'''
        f = antiformat(file)
        if not path.exists(file):
            # The file should always exist, because of how the list of files is
            # gathered, so something is wrong but we don't know what. Give up.
            raise ValueError(f'File not found: {f}')

        # Zotero stores content in the subdirectory like .../storage/N743ZXDF.
        # The item key is the alphanumeric directory name.
        # Given the key, there's no way to know whether the record is in a user
        # library or a group library, so we have to iterate over the options.
        itemkey = path.basename(path.dirname(file))
        record = None
        for library in self._libraries:
            try:
                record = library.item(itemkey)
                if __debug__: log(f'{itemkey} found in library {library.library_id}')
                break
            except zotero_errors.ResourceNotFound:
                if __debug__: log(f'{itemkey} not found in library {library.library_id}')
                continue
            except KeyboardInterrupt as ex:
                if __debug__: log(f'interrupted: {str(ex)}')
                raise
            except Exception as ex:
                if __debug__: log(f'got exception {str(ex)}')
                raise
            # pyzotero calls urllib3 for network connections. The latter uses
            # try-except clauses that broadly catch all Exceptions but don't
            # check for for KeyboardInterrupt. Thus, ^C during a network call
            # will show up as a failure to return data, not a KeyboardInterrupt.
            raise_for_interrupts()
        if not record:
            if __debug__: log(f'could not find a record for item key "{itemkey}"')
            return (None, f'Unable to retrieve Zotero record for {f}')

        # If the PDF isn't associated with a bib record, it won't have a parent.
        parentkey = self.parent_key(record, file)
        if not parentkey:
            if __debug__: log(f'file not associated with a parent record: {f}')
            return (None, f'File lacks a parent Zotero record: {f}')

        # We have an item record and a parent. We are happy campers.
        if __debug__: log(f'{parentkey} is parent of {itemkey} for {f}')
        r = ZoteroRecord(key = itemkey, parent_key = parentkey, file = file,
                         link = self.item_link(record, file), record = record)
        return (r, None)


    # For the format of the URIs, see these discussions in the Zotero forums:
    # https://forums.zotero.org/discussion/comment/335046/#Comment_335046
    # https://forums.zotero.org/discussion/78312/zotero-uri-vs-select-item

    def item_link(self, record, file):
        '''Given a record, returns an item link (i.e., "zotero://select/...)'''
        libtype = record['library']['type']
        parentkey = self.parent_key(record, file)
        if not parentkey:
            return None
        if libtype == 'user':
            return f'zotero://select/library/items/{parentkey}'
        else:
            groupid = record['library']['id']
            return f'zotero://select/groups/{groupid}/items/{parentkey}'


    def parent_key(self, record, file):
        '''Safely returns the parent key of the record item, or None.'''
        f = antiformat(file)
        if 'data' not in record:
            if __debug__: log(f'no "data" in record for {f}')
            return None
        if 'parentItem' not in record['data']:
            if __debug__: logr(f'unexpected record for {f}: ' + str(record["data"]))
            return None
        return record['data']['parentItem']
