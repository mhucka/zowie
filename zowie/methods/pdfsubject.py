'''
pdfsubject.py: write Zotero select link into the PDF file's subject property

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

class PDFSubject(WriterMethod):
    '''Implements writing Zotero links into the PDF file's Producer property.'''

    @classmethod
    def name(cls):
        return 'pdfsubject'


    @classmethod
    def description(cls):
        return ('Writes the Zotero select link into the "Subject" metadata'
                + ' field of each PDF file. If the "Subject" field is not empty'
                + ' on a given file, Zowie looks for an existing Zotero link'
                + ' within the value and updates the link if one is found;'
                + ' otherwise, Zowie leaves the field untouched unless given'
                + ' the overwrite flag (-o), in which case, it replaces the'
                + ' entire contents of the field with the Zotero select link.'
                + ' Note that the PDF "Subject" field is not the same as the'
                + ' "Title" field. For some users, the "Subject" field is not'
                + ' used for any purpose and thus can be usefully hijacked for'
                + ' storing the Zotero select link. The value is accessible'
                + ' from macOS Preview, Adobe Acrobat, DEVONthink, and'
                + ' presumably any other application that can display the PDF'
                + ' metadata fields.')


    @classmethod
    def file_extension(cls):
        return '.pdf'


    def write_link(self, file_path, uri):
        '''Write the "uri" into the Subject attribute of PDF file "file_path".'''

        fp = antiformat(file_path)
        if __debug__: log(f'reading PDF file {fp}')
        trailer = PdfReader(file_path)
        file = antiformat(f'[steel_blue3]{file_path}[/]')
        if not self.overwrite:
            subject = trailer.Info.Subject or ''
            if __debug__: log(f'found PDF Subject value {subject} on {fp}')
            if uri in subject:
                inform(f'Zotero link already present in PDF "Subject" field of {file}')
                return
            elif subject.startswith('zotero://select'):
                inform(f'Replacing existing Zotero link in PDF "Subject" field of {file}')
                subject = re.sub(r'(zotero://\S+)', uri, subject)
                trailer.Info.Subject = subject
            elif subject is not None:
                warn(f'Not overwriting existing PDF "Subject" value in {file}')
                return
            else:
                if __debug__: log(f'no prior PDF Subject field found on {fp}')
                inform(f'Writing Zotero link into PDF "Subject" field of {file}')
                trailer.Info.Subject = uri
        else:
            inform(f'Overwriting PDF "Subject" field of {file}')
            trailer.Info.Subject = uri

        if not self.dry_run:
            if __debug__: log(f'writing PDF file with new "Subject" field: {fp}')
            PdfWriter(file_path, trailer = trailer).write()
