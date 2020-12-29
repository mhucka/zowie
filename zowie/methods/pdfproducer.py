'''
pdfproducer.py: write Zotero select link into the PDF file's Producer property

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
import re

from .base import WriterMethod

if __debug__:
    from sidetrack import log


# Class definitions.
# .............................................................................

class PDFProducer(WriterMethod):
    '''Implements writing Zotero links into the PDF file's Producer property.'''

    @classmethod
    def name(cls):
        return 'pdfproducer'


    @classmethod
    def description(cls):
        return ('Writes the Zotero select link into the "Producer" metadata'
                + ' field of each PDF file. If the "Producer" field is not empty'
                + ' on a given file, Zowie looks for an existing Zotero link'
                + ' within the value and updates the link if one is found;'
                + ' otherwise, Zowie leaves the field untouched unless given'
                + ' the overwrite flag (-o), in which case, it replaces the'
                + ' entire contents of the field with the Zotero select link.'
                + ' For some users, the "Producer" field has not utility, and'
                + ' thus can be usefully hijacked for the purpose of storing'
                + ' the Zotero select link. The value is accessible from macOS'
                + ' Preview, Adobe Acrobat, DEVONthink, and presumably any'
                + ' other application that can display the PDF metadata fields.'
                + ' However, note that some users (archivists, forensics'
                + ' investigators, possibly others) do use the "Producer" field,'
                + ' and overwriting it may be undesirable.')


    @classmethod
    def file_extension(cls):
        return '.pdf'


    def write_link(self, file_path, uri):
        '''Write the "uri" into the Producer attribute of PDF file "file_path".'''

        fp = antiformat(file_path)
        if __debug__: log(f'reading PDF file {fp}')
        trailer = PdfReader(file_path)
        file = antiformat(f'[steel_blue3]{file_path}[/]')
        if not self.overwrite:
            producer = trailer.Info.Producer or ''
            if __debug__: log(f'found PDF Producer value {producer} on {fp}')
            if uri in producer:
                inform(f'Zotero link already present in PDF "Producer" field of {file}')
                return
            elif producer.startswith('zotero://select'):
                inform(f'Replacing existing Zotero link in PDF "Producer" field of {file}')
                producer = re.sub(r'(zotero://\S+)', uri, producer)
                trailer.Info.Producer = producer
            elif producer is not None:
                warn(f'Not overwriting existing PDF "Producer" value in {file}')
                return
            else:
                if __debug__: log(f'no prior PDF Producer field found on {fp}')
                inform(f'Writing Zotero link into PDF "Producer" field of {file}')
                trailer.Info.Producer = uri
        else:
            inform(f'Overwriting PDF "Producer" field of {file}')
            trailer.Info.Producer = uri

        if not self.dry_run:
            if __debug__: log(f'writing PDF file with new "Producer" field: {fp}')
            PdfWriter(file_path, trailer = trailer).write()
