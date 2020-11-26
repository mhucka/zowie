'''
Zuppa module for implementing different methods of writing Zotero links

Authors
-------

Michael Hucka <mhucka@caltech.edu> -- Caltech Library

Copyright
---------

Copyright (c) 2020 by Michael Hucka and the California Institute of Technology.
This code is open-source software released under a 3-clause BSD license.
Please see the file "LICENSE" for more information.
'''

if __debug__:
    from sidetrack import log

from .findercomment import FinderComment
from .pdfsubject import PDFSubject
from .pdfproducer import PDFProducer

KNOWN_METHODS = {
    'findercomment': FinderComment,
    'pdfsubject': PDFSubject,
    'pdfproducer': PDFProducer,
}

# Save this list to avoid recreating it all the time.
METHODS_LIST = sorted(KNOWN_METHODS.keys())

def methods_list():
    return METHODS_LIST
