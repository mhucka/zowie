'''
Zowie: a program to write Zotero select links into Zotero attachment files

Authors
-------

Michael Hucka <mhucka@caltech.edu> -- Caltech Library

Copyright
---------

Copyright (c) 2020 by Michael Hucka and the California Institute of Technology.
This code is open-source software released under a 3-clause BSD license.
Please see the file "LICENSE" for more information.
'''

from   AppKit import NSWorkspace
from   bun import inform, warn, alert, alert_fatal
from   commonpy.data_utils import DATE_FORMAT, pluralized, parsed_datetime
from   commonpy.file_utils import filename_extension, filename_basename
from   commonpy.file_utils import files_in_directory
from   commonpy.network_utils import net, network_available
from   commonpy.string_utils import antiformat
from   datetime import datetime
from   os import path
from   pathlib import Path
import sys

from .exceptions import CannotProceed
from .exit_codes import ExitCode
from .methods import KNOWN_METHODS, method_names
from .zotero import Zotero

if __debug__:
    from sidetrack import log


# Internal constants.
# .............................................................................

_IGNORED_EXT = ['.sqlite', '.sqlite-journal', '.bak', '.ico', '.json', '.csl',
                '.pl', '.js', '.css', '.config_resp']


# Exported classes.
# .............................................................................

class MainBody():
    '''Main body for Zowie.'''

    def __init__(self, **kwargs):
        '''Initialize internal state.'''

        # Assign parameters to self to make them available within this object.
        for key, value in kwargs.items():
            if __debug__: log(f'parameter value self.{key} = {value}')
            setattr(self, key, value)

        # We expose attribute "exception" that callers can use to find out
        # if the thread finished normally or with an exception.
        self.exception = None

        # Create and initialize objects for the URI writers we will use.
        self._writers = []
        for method_name in self.methods:
            method = KNOWN_METHODS[method_name](self.dry_run, self.overwrite)
            self._writers.append(method)


    def run(self):
        '''Run the main body.'''

        if __debug__: log('running MainBody')
        try:
            self._do_preflight()
            self._do_main_work()
        except Exception as ex:
            if __debug__: log(f'exception in main body: {str(ex)}')
            self.exception = sys.exc_info()
        if __debug__: log('finished MainBody')


    def stop(self):
        '''Stop the main body.'''
        if __debug__: log('stopping ...')
        pass


    def _do_preflight(self):
        '''Check the option values given by the user, and do other prep.'''

        if not network_available():
            alert_fatal('No network connection.')
            raise CannotProceed(ExitCode.no_network)

        # Sanity-check the arguments ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        hint = '(Hint: use -h for help.)'

        if not self.use_keyring and not any([self.api_key, self.user_id]):
            alert_fatal(f"Need Zotero credentials if not using keyring. {hint}")
            raise CannotProceed(ExitCode.bad_arg)
        if any(item.startswith('-') for item in self.files):
            bad = next(item for item in self.files if item.startswith('-'))
            alert_fatal(f'Unrecognized option "{bad}" in arguments. {hint}')
            raise CannotProceed(ExitCode.bad_arg)

        if self.after_date:
            try:
                # Convert user's input into a canonical format.
                self.after_date = parsed_datetime(self.after_date)
                self.after_date_str = self.after_date.strftime(DATE_FORMAT)
                if __debug__: log(f'parsed after_date as {self.after_date_str}')
            except KeyboardInterrupt as ex:
                if __debug__: log(f'got exception {str(ex)}')
                raise
            except Exception as ex:
                alert_fatal(f'Unable to parse after_date: "{str(ex)}". {hint}')
                raise CannotProceed(ExitCode.bad_arg)

        if self.file_ext:
            self.file_ext = self.file_ext.lower().split(',')
            self.file_ext = ['.' + e for e in self.file_ext if not e.startswith('.')]

        # Set up Zotero connection and gather files for work ~~~~~~~~~~~~~~~~~~

        inform('Connecting to Zotero network servers ...')
        self._zotero = Zotero(self.api_key, self.user_id, self.use_keyring)

        if len(self.files) > 1 or path.isdir(self.files[0]):
            inform('Examining folders and looking for files ...')
        # 2 passes: traverse subdirectories recursively, then filter results.
        candidates = []
        for item in self.files:
            if path.isfile(item):
                candidates.append(item)
            elif path.isdir(item):
                if __debug__: log(f'adding files in subdir {antiformat(item)}')
                candidates += files_in_directory(item)
            else:
                warn(f'Not a file nor a folder of files: "{antiformat(item)}"')
        if __debug__: log('gathering list of files ...')
        self._targets = []
        for file in candidates:
            ext = filename_extension(file)
            if path.basename(file).startswith('.') or ext in _IGNORED_EXT:
                if __debug__: log(f'ignoring ignorable file {antiformat(file)}')
                continue
            if self.file_ext and ext not in self.file_ext:
                warn(f'Skipping file without desired extension: {antiformat(file)}')
                continue
            if file_is_alias(file):
                if __debug__: log(f'ignoring macOS alias {antiformat(file)}')
                continue
            self._targets.append(file)
        if __debug__: log(f'gathered {pluralized("file", self._targets, True)}')

        if self.after_date:
            if __debug__: log(f'filtering files by date {self.after_date_str}')
            kept = []
            tzinfo = self.after_date.tzinfo
            for file in self.files:
                mtime = datetime.fromtimestamp(Path(file).stat().st_mtime)
                if mtime.replace(tzinfo = tzinfo) >= self.after_date:
                    if __debug__: log(f'keeping {file}')
                    kept.append(file)
            self._targets = kept

        if not self._targets:
            alert_fatal('No files to process; quitting.')
            raise CannotProceed(ExitCode.bad_arg)


    def _do_main_work(self):
        if self.overwrite:
            warn('Overwrite mode in effect.')
        if self.dry_run:
            warn('Running in dry run mode – will not modify files.')
        inform(f'Will process {pluralized("file", self._targets, True)}'
               + f' using {pluralized("method", self.methods)}'
               + f' [cyan2]{", ".join(self.methods)}[/].')
        if len(self._targets) > 10000:
            inform("(That's a huge number of files – this will take a long time.)")
        elif len(self._targets) > 1000:
            inform("(That's a lot of files – this will take some time.)")

        for file in self._targets:
            (record, failure) = self._zotero.record_for_file(file)
            if failure:
                warn(failure)
                continue
            ext = filename_extension(file)
            for method in self._writers:
                if method.file_extension() and ext != method.file_extension():
                    f = antiformat(f'[steel_blue3]{file}[/]')
                    warn(f"Method [cyan2]{method.name()}[/] can't be used on {f}")
                else:
                    method.write_link(file, record.link)


# Misc. utilities
# .............................................................................

_WORKSPACE = NSWorkspace.sharedWorkspace()

# The code below is based in part on code posted by user "kuzzoooroo" on
# 2014-01-23 to Stack Overflow at https://stackoverflow.com/a/21245832/743730

def file_is_alias(item):
    '''Returns True if the given "item" is a macOS Alias file.'''
    # mac alias files test positive as files but negative as links.
    if path.islink(item) or not path.isfile(item):
        return False
    uti, err = _WORKSPACE.typeOfFile_error_(path.realpath(item), None)
    if err:
        return False
    else:
        return uti == "com.apple.alias-file"
