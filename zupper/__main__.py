'''
Zupper: a program to write Zotero item URIs into Zotero article PDF files

Authors
-------

Michael Hucka <mhucka@caltech.edu> -- Caltech Library

Copyright
---------

Copyright (c) 2020 by Michael Hucka and the California Institute of Technology.
This code is open-source software released under a 3-clause BSD license.
Please see the file "LICENSE" for more information.
'''

from   boltons.debugutils import pdb_on_signal
import os
from   os import path, cpu_count
import plac
import signal
import sys
from   sys import exit as exit

if __debug__:
    from sidetrack import set_debug, log, logr

import zupper
from zupper import print_version
from .exceptions import *
from .exit_codes import ExitCode
from .ui import inform, warn, alert, alert_fatal

# .............................................................................

@plac.annotations(
    no_color   = ('do not color-code terminal output',                 'flag',   'C'),
    no_comment = ('do not write URI into macOS Finder comment',        'flag',   'F'),
    lastmod    = ('ignore file whose modification dates predate "L"',  'option', 'l'),
    quiet      = ('only print important messages while working',       'flag',   'q'),
    watch      = ('continuously watch for new files and update them',  'flag',   'w'),
    version    = ('print version info and exit',                       'flag',   'V'),
    debug      = ('write detailed trace to "OUT" ("-" means console)', 'option', '@'),
    files      = 'file(s) and/or folder(s) containing Zotero article PDF files',
)

def main(no_color = False, quiet = False, version = False, debug = 'OUT', files):
    '''Zupper (a loose acronym of "Zotero URIs into PDF Properties").

Zupper writes Zotero item URIs into the metadata of PDF files.  It also adds
the URIs to the files' macOS Spotlight file comments.

Credentials for Zotero access
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


Basic usage
~~~~~~~~~~~


Watch mode
~~~~~~~~~~


Additional command-line arguments
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If given the -q option, Zupper will not print its usual informational messages
while it is working.  It will only print messages for warnings or errors.
By default messages printed by Zupper are also color-coded.  If given the
option -C, Zupper will not color the text of messages it prints.  (This latter
option is useful when running Zupper within subshells inside other environments
such as Emacs.)

If given the -V option, this program will print the version and other
information, and exit without doing anything else.

If given the -@ argument, this program will output a detailed trace of what it
is doing.  The debug trace will be sent to the given destination, which can
be '-' to indicate console output, or a file path to send the output to a file.

When -@ has been given, Zupper also installs a signal handler on signal SIGUSR1
that will drop Zupper into the pdb debugger if the signal is sent to the
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

    # Initial setup -----------------------------------------------------------

    ui = UI('Zupper', 'Zotero URIs into PDF Properties',
            use_color = not no_color, be_quiet = quiet)
    ui.start()

    if debug != 'OUT':
        if __debug__: set_debug(True, debug)
        import faulthandler
        faulthandler.enable()
        if not sys.platform.startswith('win'):
            # Even with a different signal, I can't get this to work on Win.
            pdb_on_signal(signal.SIGUSR1)

    # Preprocess arguments and handle early exits -----------------------------

    if version:
        print_version()
        exit(int(ExitCode.success))

    # Do the real work --------------------------------------------------------

    if __debug__: log('='*8 + f' started {timestamp()} ' + '='*8)
    body = exception = None
    try:
        pass
    except Exception as ex:
        exception = sys.exc_info()

    # Try to deal with exceptions gracefully ----------------------------------

    exit_code = ExitCode.success
    if exception:
        if exception[0] == CannotProceed:
            exit_code = exception[1].args[0]
        elif exception[0] in [KeyboardInterrupt, UserCancelled]:
            if __debug__: log(f'received {exception.__class__.__name__}')
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
    if exit_code == ExitCode.user_interrupt:
        os._exit(int(exit_code))
    else:
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
