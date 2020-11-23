'''
keyring_utils.py: utilities for reading and writing credentials to the keyring

Authors
-------

Michael Hucka <mhucka@caltech.edu> -- Caltech Library

Copyright
---------

Copyright (c) 2020 by Michael Hucka and the California Institute of Technology.
This code is open-source software released under a 3-clause BSD license.
Please see the file "LICENSE" for more information.
'''

import getpass
import keyring
import sys

if sys.platform.startswith('win'):
    import keyring.backends
    from keyring.backends.Windows import WinVaultKeyring


# Global constants.
# .............................................................................

_KEYRING = f'org.caltechlibrary.{__package__}'
'''The name of the keyring used to store server access credentials, if any.'''


# Main functions.
# .............................................................................

def keyring_credentials(lib_type, lib_id):
    '''Looks up the user's credentials.'''
    if sys.platform.startswith('win'):
        keyring.set_keyring(WinVaultKeyring())
    if sys.platform.startswith('darwin'):
        keyring.set_keyring(Keyring())
    value = keyring.get_password(_KEYRING, lib_type + ':' + lib_id)
    return _decoded(value) if value else (None, None, None)


def save_keyring_credentials(api_key, lib_type, lib_id):
    '''Saves the user's credentials.'''
    if sys.platform.startswith('win'):
        keyring.set_keyring(WinVaultKeyring())
    if sys.platform.startswith('darwin'):
        keyring.set_keyring(Keyring())
    keyring.set_password(_KEYRING, 'zupper', _encoded(api_key, lib_type, lib_id))


# Utility functions.
# .............................................................................

# Explanation about the weird way this is done: the Python keyring module
# only offers a single function for setting a value; ostensibly, this is
# intended to store a password associated with an identifier (a user name),
# and this identifier is expected to be obtained some other way, such as by
# using the current user's computer login name.  But, in our situation, we
# have multiple pieces of information we have to store: the library id, the
# library type, and the api key.  The hackacious solution taken here is to
# concatenate several values into a single string used as the actual value
# stored.  The individual values are separated by a character that is
# unlikely to be part of any user-typed value.

_sep = ''
'''Character used to separate multiple actual values stored as a single
encoded value string.  This character is deliberately chosen to be something
very unlikely to be part of a legitimate string value typed by user at a
shell prompt, because control-c is normally used to interrupt programs.
'''

def _encoded(api_key, lib_type, lib_id):
    return f'{api_key}{_sep}{lib_type}{_sep}{lib_id}'


def _decoded(value_string):
    return tuple(value_string.split(_sep))


def password(prompt):
    # If it's a tty, use the version that doesn't echo the password.
    if sys.stdin.isatty():
        return getpass.getpass(prompt)
    else:
        sys.stdout.write(prompt)
        sys.stdout.flush()
        return sys.stdin.readline().rstrip()


def validated_input(msg, default_value, is_valid):
    while True:
        if __debug__: log(f'asking user: "{msg} [{default_value}]"')
        default = (' [' + default_value + ']') if default_value else ''
        value = input(msg + default + ': ')
        if is_valid(value):
            if __debug__: log(f'got "{value}" from user')
            return value
        else:
            alert(f'"{value}" does not appear valid for {msg}')
