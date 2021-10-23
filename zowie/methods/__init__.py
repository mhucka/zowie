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

def method_names():
    return ['findercomment', 'wherefrom', 'pdfsubject', 'pdfproducer']


def method_object(name):
    # This grungy approach, instead of using a dictionary, is on purpose: it
    # implements delayed loading of methods in order to speed up application
    # start time.
    if name == 'findercomment':
        from .findercomment import FinderComment
        return FinderComment
    elif name == 'wherefrom':
        from .wherefrom import WhereFrom
        return WhereFrom
    elif name == 'pdfsubject':
        from .pdfsubject import PDFSubject
        return PDFSubject
    elif name == 'pdfproducer':
        from .pdfproducer import PDFProducer
        return PDFProducer
    else:
        raise ValueError(f'Unknown method name "{name}"')
