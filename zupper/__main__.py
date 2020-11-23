'''
Zuppa: a program to write Zotero item URIs into Zotero article PDF files

Authors
-------

Michael Hucka <mhucka@caltech.edu> -- Caltech Library

Copyright
---------

Copyright (c) 2020 by Michael Hucka and the California Institute of Technology.
This code is open-source software released under a 3-clause BSD license.
Please see the file "LICENSE" for more information.
'''

from   commonpy.data_utils import timestamp
from   commonpy.interrupt import config_interrupt
from   boltons.debugutils import pdb_on_signal
import os
from   os import path, cpu_count
import plac
from   quiche import UI, inform, warn, alert, alert_fatal
import signal
import sys
from   sys import exit as exit

if __debug__:
    from sidetrack import set_debug, log, logr

import zuppa
from zuppa import print_version
from .exceptions import *
from .exit_codes import ExitCode
from .main_body import MainBody

# .............................................................................

@plac.annotations(
    api_key    = ('use API key "A" to access the Zotero API service',        'option', 'a'),
    after_date = ('only act on files created or modified after date "D"',    'option', 'd'),
    identifier = ('Zotero library identifier',                               'option', 'i'),
    methods    = ('select how the URIs are to be stored (default: link)',    'option', 'm'),
    dry_run    = ('report what would be done without actually doing it',     'flag',   'n'),
    quiet      = ('be less chatty -- only print important messages',         'flag',   'q'),
    version    = ('print version info and exit',                             'flag',   'V'),
    watch_mode = ('continuously watch for new files and update them',        'flag',   'w'),
    no_keyring = ('do not store credentials in a keyring service',           'flag',   'X'),
    no_color   = ('do not color-code terminal output',                       'flag',   'Y'),
    debug      = ('write detailed trace to "OUT" ("-" means console)',       'option', '@'),
    files      = 'file(s) and/or folder(s) containing Zotero article PDF files',
)

def main(api_key = 'A', after_date = 'D', identifier = 'I', methods = 'M',
         dry_run = False, quiet = False, version = False, watch_mode = False,
         no_keyring = False,  no_color = False, debug = 'OUT', *files):
    '''Zuppa (a loose acronym of "Zotero URIs into PDF Properties").

Zuppa writes Zotero item URIs into the metadata of PDF files.  It also adds
the URIs to the files' macOS Spotlight file comments.

Credentials for Zotero access
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Zuppa needs a library identifier and API key in order to retrieve information
about your Zotero entries.  By default, it tries to get this information from
the system keychain.  If the information does not exist in the keychain from a
previous run of Zuppa, it will ask the user interactively for the identifier
and API key, and (unless the -K option is given) store them in the user's
keychain so that it does not have to ask again in the future.  It is also
possible to supply the information directly on the command line using the
-i and -a options; the given values will override the values stored in the
keychain.  (This is also how you can replace previously-stored values: use
-i and/or -a, without -K, and the new values will override the stored values.)

When using the -i option, the library identifier can be prefixed with the
string "user:" or "group:" to indicate whether the identifier refers to a
personal or group library.  For example,

  zuppa -i user:1234578 ...

If -i is used and the value does not begin with "user:" or "group:", then it
is assumed to be a personal library identifier.

Basic usage
~~~~~~~~~~~

The most convenient way to run Zuppa is to let it store your credentials in
your keychain so that you do not have to provide them each time or write them
on the command line.


Watch mode
~~~~~~~~~~

If given the option -w, Zuppa will go into continuous watch mode: instead
of exiting after processing the arguments (i.e., gathering a list of PDF files,
filtering by last modification date, and updating file metadata), it will keep
running and watching for changes in any of the arguments.  If any files are
modified or added (including files within any folders listed on the command
line), Zuppa repeats its normal processing for them.  For example:

  zuppa -f -w ~/zotero/storage

will start Zuppa in watch mode on a Zotero storage directory, with the
--finder-too option to update both the PDF files and the Finder comments.


Additional command-line arguments
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If given the -q option, Zuppa will not print its usual informational messages
while it is working.  It will only print messages for warnings or errors.
By default messages printed by Zuppa are also color-coded.  If given the
option -C, Zuppa will not color the text of messages it prints.  (This latter
option is useful when running Zuppa within subshells inside other environments
such as Emacs.)

If given the -V option, this program will print the version and other
information, and exit without doing anything else.

If given the -@ argument, this program will output a detailed trace of what it
is doing.  The debug trace will be sent to the given destination, which can
be '-' to indicate console output, or a file path to send the output to a file.

When -@ has been given, Zuppa also installs a signal handler on signal SIGUSR1
that will drop Zuppa into the pdb debugger if the signal is sent to the
running process.


Return values
~~~~~~~~~~~~~

This program exits with a return code of 0 if no problems are encountered.
It returns a nonzero value otherwise. The following table lists the possible
return values:

    0 = success -- program completed normally
    1 = the user interrupted the program's execution
    2 = encountered a bad or missing value for an option
    3 = no network detected -- cannot proceed
    4 = file error -- encountered a problem with a file
    5 = server error -- encountered a problem with a server
    6 = an exception or fatal error occurred

Command-line arguments summary
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
'''

    # Set up debug logging as soon as possible, if requested ------------------

    if debug != 'OUT':
        if __debug__: set_debug(True, debug)
        import faulthandler
        faulthandler.enable()
        if not sys.platform.startswith('win'):
            # Even with a different signal, I can't get this to work on Win.
            pdb_on_signal(signal.SIGUSR1)

    # Preprocess arguments and handle early exits -----------------------------

    ui = UI('Zuppa', 'Zotero URI PDF Property Annotator',
            use_color = not no_color, be_quiet = quiet)
    ui.start()

    if version:
        print_version()
        exit(int(ExitCode.success))

    # Do the real work --------------------------------------------------------

    if __debug__: log('='*8 + f' started {timestamp()} ' + '='*8)
    body = exception = None
    try:
        body = MainBody(files       = files,
                        api_key     = None if api_key == 'A' else api_key,
                        library_id  = None if identifier == 'I' else identifier,
                        after_date  = None if after_date == 'D' else after_date,
                        use_keyring = not no_keyring,
                        methods     = methods,
                        watch_mode  = watch_mode,
                        dry_run     = dry_run)
        config_interrupt(body.stop, UserCancelled(ExitCode.user_interrupt))
        body.run()
        exception = body.exception
    except Exception as ex:
        exception = sys.exc_info()

    # Try to deal with exceptions gracefully ----------------------------------

    exit_code = ExitCode.success
    if exception:
        if __debug__: log(f'main body returned an exception: {exception}')
        if exception[0] == CannotProceed:
            exit_code = exception[1].args[0]
        elif exception[0] in [KeyboardInterrupt, UserCancelled]:
            warn('Interrupted.')
            exit_code = ExitCode.user_interrupt
        else:
            msg = str(exception[1])
            alert_fatal(f'Encountered error {exception[0].__name__}: {msg}')
            exit_code = ExitCode.exception
            if __debug__:
                from traceback import format_exception
                details = ''.join(format_exception(*exception))
                logr(f'Exception: {msg}\n{details}')
    else:
        inform('Done.')

    # And exit ----------------------------------------------------------------

    if __debug__: log('_'*8 + f' stopped {timestamp()} ' + '_'*8)
    if __debug__: log(f'exiting with exit code {exit_code}')
    exit(int(exit_code))


# Main entry point.
# .............................................................................

# The following entry point definition is for the console_scripts keyword
# option to setuptools.  The entry point for console_scripts has to be a
# function that takes zero arguments.
def console_scripts_main():
    plac.call(main)

# The following allows users to invoke this using "python3 -m handprint".
if __name__ == '__main__':
    plac.call(main)
