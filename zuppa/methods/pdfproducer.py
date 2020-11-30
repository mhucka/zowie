'''
pdfproducer.py: write Zotero URI into the PDF file's Producer property

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

class PDFProducer(WriterMethod):
    '''Implements writing Zotero URIs into the PDF file's Producer property.'''

    @classmethod
    def name(self):
        return 'pdfproducer'


    @classmethod
    def description(self):
        return ('Rewrites the PDF "Producer" metadata field in the file. For'
                + ' some users, this field has not utility, and thus can be'
                + ' usefully hijacked for the purpose of storing the Zotero'
                + ' item URI. This makes the value accessible from macOS'
                + ' Preview, Adobe Acrobat, DEVONthink, and presumably any'
                + ' other application that can read the PDF metadata fields.'
                + ' However, note that some users (archivists, forensics'
                + ' investigators, possibly others) may in fact use the'
                + ' Producer field, and overwriting it may be undesirable.')


    def write_uri(self, file, uri, dry_run):
        '''Write the "uri" into the Producer attribute of PDF file "file".
        The previous value will be overwritten.
        '''
        if __debug__: log(f'reading PDF file {file}')
        path = antiformat(f'[grey89]{file}[/]')
        trailer = PdfReader(file)
        producer = trailer.Info.Producer
        if producer:
            if __debug__: log(f'read PDF Producer value {producer} on {file}')
            if uri in producer:
                inform(f'Zotero URI already present in PDF "Producer" field of {path}')
                return
            elif producer.startswith('zotero://select'):
                warn(f'Replacing existing Zotero URI in PDF "Producer" field of {path}')
            else:
                warn(f'Overwriting PDF "Producer" field of {path}')
        else:
            if __debug__: log(f'no prior PDF Producer field found on {file}')
            inform(f'Writing Zotero URI into PDF "Producer" field of {path}')

        trailer.Info.Producer = uri
        if not dry_run:
            if __debug__: log(f'writing PDF file with new Producer field: {file}')
            PdfWriter(file, trailer = trailer).write()
