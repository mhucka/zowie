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
from pyzotero import zotero

if __debug__:
    from sidetrack import log

from .exit_codes import ExitCode
from .keyring_utils import keyring_credentials, save_keyring_credentials
from .keyring_utils import validated_input


# Exported classes.
# .............................................................................

class Zotero():
    def __init__(self, key, user_id, use_keyring):
        if key and not key.isalnum():
            alert_fatal(f'"{key}" does not appear to be a valid API key')
            raise CannotProceed(ExitCode.bad_arg)
        if user_id and not user_id.isdigit():
            alert_fatal(f'"{user_id}" does not appear to be a Zotero user ID')
            raise CannotProceed(ExitCode.bad_arg)

        # If the user supplied all the values on the command line, those are
        # the values used.  If none were supplied by the user on the command
        # line, all the values are retrieved from the user's keyring.  If
        # some were supplied and others missing, they're filled in from
        # either the keyring or by prompting the user.

        if __debug__: log('keyring {}', 'enabled' if use_keyring else 'disabled')
        if key and user_id and use_keyring:
            # Given values for everything. Save them if desired.
            if __debug__: log('saving new credentials to keyring')
            save_keyring_credentials(key, user_id)
        else:
            # Given some values but not all. Look up the rest & use as defaults.
            k_key, k_id = keyring_credentials() if use_keyring else (None, None)
            if not key:
                key = validated_input('API key', k_key, lambda x: x.isalnum())
            if not user_id:
                user_id = validated_input('User ID', k_id, lambda x: x.isdigit())
            if use_keyring:
                if __debug__: log('saving new credentials to keyring')
                save_keyring_credentials(key, user_id)

        self._key = key
        self._user_id = user_id

        # Get connected and store the Zotero conection object.
        try:
            if __debug__: log(f'connecting to Zotero as user {user_id}')
            self._zotero = zotero.Zotero(user_id, 'user', key)
        except Exception as ex:
            if __debug__: log(f'failed to create Zotero user object: str(ex)')
            alert_fatal('Unable to connect to Zotero API')
            raise

        # Look up all the group id's that the user can use and store them.
        self._group_ids = []
        for group in self._zotero.groups():
            if __debug__: log(f'user can access group id {group["id"]}')
            self._group_ids.append(group['id'])
