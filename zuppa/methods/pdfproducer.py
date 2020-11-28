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

from   bun import inform
from   pdfrw import PdfReader, PdfWriter

if __debug__:
    from sidetrack import log

from .base import WriterMethod


# Class definitions.
# .............................................................................

class PDFProducer(WriterMethod):
    def name(self):
        return 'pdfproducer'


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
        trailer = PdfReader(file)
        trailer.Info.Producer = uri
        if not dry_run:
            if __debug__: log(f'writing PDF file with new Producer field: {file}')
            PdfWriter(file, trailer = trailer).write()
