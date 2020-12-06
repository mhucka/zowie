'''
Zowie module for implementing different methods of writing Zotero links

Authors
-------

Michael Hucka <mhucka@caltech.edu> -- Caltech Library

Copyright
---------

Copyright (c) 2020 by Michael Hucka and the California Institute of Technology.
This code is open-source software released under a 3-clause BSD license.
Please see the file "LICENSE" for more information.
'''

from .findercomment import FinderComment
from .pdfsubject import PDFSubject
from .pdfproducer import PDFProducer
from .wherefrom import WhereFrom

KNOWN_METHODS = {
    'findercomment': FinderComment,
    'wherefrom': WhereFrom,
    'pdfsubject': PDFSubject,
    'pdfproducer': PDFProducer,
}

# Save this list to avoid recreating it all the time.
_METHOD_NAMES = sorted(KNOWN_METHODS.keys())

def method_names():
    return _METHOD_NAMES
