'''
pdfsubject.py: write Zotero URI into the PDF file's subject property

Authors
-------

Michael Hucka <mhucka@caltech.edu> -- Caltech Library

Copyright
---------

Copyright (c) 2020 by Michael Hucka and the California Institute of Technology.
This code is open-source software released under a 3-clause BSD license.
Please see the file "LICENSE" for more information.
'''

from   bun import inform, warn
from   commonpy.string_utils import antiformat
from   pdfrw import PdfReader, PdfWriter

if __debug__:
    from sidetrack import log

from .base import WriterMethod


# Class definitions.
# .............................................................................

class PDFSubject(WriterMethod):
    '''Implements writing Zotero URIs into the PDF file's Producer property.'''

    @classmethod
    def name(self):
        return 'pdfsubject'


    @classmethod
    def description(self):
        return ('Rewrites the PDF "Subject" metadata field in the file. This'
                + ' is not the same as the Title field. For some users, the'
                + ' Subject field is not used for any other purpose and thus'
                + ' can be usefully hijacked for the purpose of storing the'
                + ' Zotero item URI. This makes the value accessible from'
                + ' macOS Preview, Adobe Acrobat, DEVONthink, and presumably'
                + ' any other application that can read the PDF metadata'
                + ' fields.')


    def write_uri(self, file, uri, dry_run, overwrite):
        '''Write the "uri" into the Subject attribute of PDF file "file".
        The previous value will be overwritten.
        '''
        path = antiformat(f'[grey89]{file}[/]')
        if __debug__: log(f'reading PDF file {file}')
        trailer = PdfReader(file)
        subject = trailer.Info.Subject
        if not overwrite:
            if subject:
                if __debug__: log(f'read PDF Subject value {subject} on {file}')
                if uri in subject:
                    inform(f'Zotero URI already present in PDF "Subject" field of {path}')
                    return
                elif subject.startswith('zotero://select'):
                    warn(f'Replacing existing Zotero URI in PDF "Subject" field of {path}')
                else:
                    # Overwrite mode is not on, so user might not expect this.
                    warn(f'Overwriting PDF "Subject" field of {path}')
            else:
                if __debug__: log(f'no prior PDF Subject field found on {file}')
                inform(f'Writing Zotero URI into PDF "Subject" field of {path}')
        else:
            inform(f'Overwriting PDF "Subject" field of {path}')

        trailer.Info.Subject = uri
        if not dry_run:
            if __debug__: log(f'writing PDF file with new Subject field: {file}')
            PdfWriter(file, trailer = trailer).write()
