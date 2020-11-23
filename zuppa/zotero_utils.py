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

from quiche import inform, warn, alert, alert_fatal

if __debug__:
    from sidetrack import log

from .exit_codes import ExitCode
from .keyring_utils import keyring_credentials, save_keyring_credentials


def zotero_credentials(key, library_id, use_keyring):
    '''Return a tuple of (key, type, id) for the user's Zotero access.

    If the user supplied all the values on the command line, those are the
    values returned.  If none were supplied by the user on the command
    line, all the values are retrieved from the user's keyring.  If some
    were supplied and others missing, they're filled in from either the
    keyring or by prompting the user.
    '''
    if key and not key.isalnum():
        alert_fatal(f'"{key}" does not appear to be a valid API key')
        raise CannotProceed(ExitCode.bad_arg)
    if library_id:
        libtype, libid = library_id.split(':')
        if not libid.isdigit():
            alert_fatal(f'"{libid}" does not appear to be a Zotero library id')
            raise CannotProceed(ExitCode.bad_arg)
        if libtype not in ['user', 'group']:
            warn(f'Unrecognized library type "{libtype}" -- using "user"')
            libtype = 'user'
    else:
        libtype, libid = None, None
    key = key
    if __debug__: log('keyring {}', 'enabled' if use_keyring else 'disabled')
    if all([key, libid, libtype]):
        # Given values for everything. Save them if desired.
        if use_keyring:
            if __debug__: log('saving new credentials to keyring')
            save_keyring_credentials(key, libtype, libid)
    elif any([key, libtype, libid]):
        # Given some values but not all. Look up the rest & use as defaults.
        saved_key, saved_type, saved_id = None, None, None
        if use_keyring:
            if __debug__: log(f'getting credentials from keyring')
            saved_key, saved_type, saved_id = keyring_credentials()


            # Problem: turns out pdfs in storage/ are mixed for group
            # and personal library.  Need to ask the user for all their
            # library id's


            key, libtype, libid = credentials_from_user(
                key or saved_key, libtype or saved_type, libid or saved_id)





        if use_keyring:
            if __debug__: log('saving new credentials to keyring')
            save_keyring_credentials(key, libtype, libid)
    else:
        # We were given nothing, so get it from the keyring
        key, libtype, libid = keyring_credentials()
    return key, libtype, libid



def credentials_from_user(key, libtype, libid):
    if not key:
        key = validated_input('API key', key, lambda x: x.isalphanum())
    if not libid:
        libid = validated_input('Library ID', libid, lambda x: x.isdigit())
    if not libtype:
        libtype = validated_input('Type ("user" or "group")', libtype,
                                   lambda x: x.lower() in ['user', 'group'])
        libtype = libtype.lower()
    return key, libtype, libid




def library_type(id_string):
    if ':' in id_string:
        lib_type, lib_id = id_string.split(':')
        if lib_type not in ['user', 'group']:
            warn(f'Unrecognized library type "{lib_type}" -- defaulting to "user"')
            return 'user', lib_id
        else:
            return lib_type, lib_id
    else:
        return 'user', id_string
