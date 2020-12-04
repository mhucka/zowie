'''
Zowie: a program to write Zotero select links into article PDF files

Authors
-------

Michael Hucka <mhucka@caltech.edu> -- Caltech Library

Copyright
---------

Copyright (c) 2020 by Michael Hucka and the California Institute of Technology.
This code is open-source software released under a 3-clause BSD license.
Please see the file "LICENSE" for more information.
'''

from   bun import UI, inform, warn, alert, alert_fatal
from   commonpy.data_utils import timestamp
from   commonpy.interrupt import config_interrupt
from   commonpy.string_utils import antiformat
from   boltons.debugutils import pdb_on_signal
import os
from   os import path, cpu_count
import plac
import signal
import shutil
import sys
from   sys import exit as exit
from   textwrap import wrap

if __debug__:
    from sidetrack import set_debug, log, logr

import zowie
from zowie import print_version
from .exceptions import *
from .exit_codes import ExitCode
from .main_body import MainBody
from .methods import method_names, KNOWN_METHODS

# .............................................................................

@plac.annotations(
    api_key    = ('API key to access the Zotero API service',                'option', 'a'),
    no_color   = ('do not color-code terminal output',                       'flag',   'C'),
    after_date = ('only act on files created or modified after date "D"',    'option', 'd'),
    identifier = ('Zotero user ID for API calls',                            'option', 'i'),
    no_keyring = ('do not store credentials in the keyring service',         'flag',   'K'),
    list       = ('print list of known methods',                             'flag',   'l'),
    method     = ('select method to store links (default: finder comments)', 'option', 'm'),
    dry_run    = ('report what would be done without actually doing it',     'flag',   'n'),
    overwrite  = ('forcefully overwrite previous content',                   'flag',   'o'),
    quiet      = ('be less chatty -- only print important messages',         'flag',   'q'),
    version    = ('print version info and exit',                             'flag',   'V'),
    debug      = ('write detailed trace to "OUT" ("-" means console)',       'option', '@'),
    files      = 'file(s) and/or folder(s) containing Zotero article PDF files',
)

def main(api_key = 'A', no_color = False, after_date = 'D', identifier = 'I',
         no_keyring = False,  list = False, method = 'M', dry_run = False,
         overwrite = False, quiet = False, version = False, debug = 'OUT', *files):
    '''Zowie ("ZOtero link WrItEr") is a tool for Zotero users.

Zowie writes Zotero select links into the PDF files and/or the macOS Finder
metadata attributes of PDF files in the user's Zotero database. This makes it
possible to look up the Zotero entry of a PDF file from outside of Zotero.

Credentials for Zotero access
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Zowie needs to know the user's personal library identifier (also known as the
"userID") and a Zotero API key. By default, it tries to get this information
from the user's keychain. If the values do not exist in the keychain from a
previous run, Zowie will ask the user, and (unless the -K option is given)
store the values in the user's keychain so that it does not have to ask again
in the future. It is also possible to supply the identifier and API key on
the command line using the -i and -a options, respectively; the given values
will then override the values stored in the keychain (unless the -K option is
also given). This is also how you can replace previously-stored values: use
-i and -a (without -K) and the new values will override the stored values.

To find out your Zotero userID and create an API key, log in to your Zotero
account at Zotero.org and visit https://www.zotero.org/settings/keys

Basic usage
~~~~~~~~~~~

Zowie can operate on a folder, or one or more individual PDF files, or a mix
of both. Suppose your local Zotero database is located in ~/my-zotero/. Perhaps
the simplest way to run Zowie is the following command:

  zowie ~/my-zotero

If this is your first run of Zowie, it will ask you for your userID and API
key, then search for PDF files recursively under ~/my-zotero/.  For each PDF
file found, Zowie will contact the Zotero servers over the network and
determine the Zotero URI for the bibliographic entry containing that PDF
file. Finally, it will use its default method of writing the Zotero select
link, which is to write it into the macOS Finder comments for the file.

Instead of a folder, you can invoke zowie on one or more individual files (but
be careful to quote pathnames with spaces in them, such as in this example):

  zowie "~/my-zotero/storage/26GS7CZL/Smith 2020 Paper.pdf"

Methods of writing the Zotero select link
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Zowie supports multiple methods of writing the Zotero select link.  The
option -l will cause Zowie to print a list of all the methods available,
then exit. The default is to write it into Finder comments for the file.
(These comments are visible in the Finder's "Get Info" panel for the file.)

The option -m can be used to select one or more methods when running
Zowie. Separate the method names with commas, without spaces. For example, the
following command will make Zowie write the Zotero select link into the Finder
comments as well as the "Where from" attribute:

  zowie -m findercomment,wherefrom ~/my-zotero/storage

Where possible, Zowie tries to preserve the previous contents of metadata
attributes.  For example, In the case of Finder comments and "Where from", it
looks for existing Zotero links in the contents and updates those links only;
if it does not find an existing Zotero link, it prepends one instead of
replacing the value completely.  The general rule is that Zowie will try to
detect whether a Zotero select link is already present in the chosen metadata
attribute(s) and will only update the link text if a link is found;
otherwise, it will not write the Zotero select link at all unless given the
overwrite (-o) option.  The overwrite option (-o) makes Zowie replace values
completely.  Check the description of the methods for more details about what
they do by default and the impact of the -o option.

Filtering by date
~~~~~~~~~~~~~~~~~

If the -d option is given, the PDF files will be filtered to use only those
whose last-modified date/time stamp is no older than the given date/time
description. Valid descriptors are those accepted by the Python dateparser
package. Make sure to enclose descriptions within single or double
quotes. Examples:

 zowie -d "2 weeks ago" ....
 zowie -d "2014-08-29" ....
 zowie -d "12 Dec 2014" ....
 zowie -d "July 4, 2013" ....

Additional command-line arguments
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If given the -n ("dry run") option, Zowie will only print what it would do
without actually doing it.

If given the -q option, Zowie will not print its usual informational messages
while it is working. It will only print messages for warnings or errors.
By default messages printed by Zowie are also color-coded. If given the
option -C, Zowie will not color the text of messages it prints. (This latter
option is useful when running Zowie within subshells inside other environments
such as Emacs.)

If given the -V option, this program will print the version and other
information, and exit without doing anything else.

If given the -@ argument, this program will output a detailed trace of what it
is doing. The debug trace will be sent to the given destination, which can
be '-' to indicate console output, or a file path to send the output to a file.

When -@ has been given, Zowie also installs a signal handler on signal SIGUSR1
that will drop Zowie into the pdb debugger if the signal is sent to the
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

    ui = UI('Zowie', 'ZOtero link WrItEr', use_color = not no_color, be_quiet = quiet)
    ui.start()

    if version:
        print_version()
        exit(int(ExitCode.success))
    if list:
        inform('Known methods:\n')
        width = (shutil.get_terminal_size().columns - 2) or 78
        for name in method_names():
            text = f'[cyan2]{name}[/]: ' + KNOWN_METHODS[name].description()
            inform('\n'.join(wrap(text, width = width, subsequent_indent = '  ')))
            inform('')
        exit(int(ExitCode.success))

    methods_list = ['findercomment'] if method == 'M' else method.lower().split(',')

    # Do the real work --------------------------------------------------------

    if __debug__: log('='*8 + f' started {timestamp()} ' + '='*8)
    body = exception = None
    try:
        body = MainBody(files       = files,
                        api_key     = None if api_key == 'A' else api_key,
                        user_id     = None if identifier == 'I' else identifier,
                        use_keyring = not no_keyring,
                        after_date  = None if after_date == 'D' else after_date,
                        methods     = methods_list,
                        dry_run     = dry_run,
                        overwrite   = overwrite)
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
            msg = antiformat(str(exception[1]))
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
