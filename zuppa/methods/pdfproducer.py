'''
pdfproducer.py: write Zotero URI into the PDF file's producer property

Authors
-------

Michael Hucka <mhucka@caltech.edu> -- Caltech Library

Copyright
---------

Copyright (c) 2020 by Michael Hucka and the California Institute of Technology.
This code is open-source software released under a 3-clause BSD license.
Please see the file "LICENSE" for more information.
'''

from .base import WriterMethod

if __debug__:
    from sidetrack import log


# Class definitions.
# .............................................................................

class PDFProducer(WriterMethod):
    def name(self):
        return 'pdfproducer'


    def write_uri(self, file, uri):
        pass