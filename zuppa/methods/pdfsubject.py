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

from   bun import inform
from   pdfrw import PdfReader, PdfWriter

if __debug__:
    from sidetrack import log

from .base import WriterMethod


# Class definitions.
# .............................................................................

class PDFSubject(WriterMethod):
    def name(self):
        return 'pdfsubject'


    def write_uri(self, file, uri, dry_run):
        '''Write the "uri" into the Subject attribute of PDF file "file".
        The previous value will be overwritten.
        '''
        if __debug__: log(f'reading PDF file {file}')
        trailer = PdfReader(file)
        trailer.Info.Subject = uri
        if not dry_run:
            if __debug__: log(f'writing PDF file with new subject field: {file}')
            PdfWriter(file, trailer = trailer).write()
