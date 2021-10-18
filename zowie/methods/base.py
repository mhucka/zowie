'''
base.py: base class definition for annotation methods in Zowie

Authors
-------

Michael Hucka <mhucka@caltech.edu> -- Caltech Library

Copyright
---------

Copyright (c) 2020 by Michael Hucka and the California Institute of Technology.
This code is open-source software released under a 3-clause BSD license.
Please see the file "LICENSE" for more information.
'''

from abc import ABC, abstractmethod

if __debug__:
    from sidetrack import log


# Class definitions.
# .............................................................................
# Basics for the __eq__ etc. methods came from
# https://stackoverflow.com/questions/1061283/lt-instead-of-cmp

class WriterMethod(ABC):
    '''Base class for Zotero select link writer methods.'''

    def __init__(self, dry_run = False, overwrite = False, add_space = False):
        self.dry_run = dry_run
        self.overwrite = overwrite
        self.add_space = add_space


    def __str__(self):
        return self.name()


    def __repr__(self):
        return self.name()


    def __eq__(self, other):
        if isinstance(other, type(self)):
            return self.__dict__ == other.__dict__
        return NotImplemented


    def __ne__(self, other):
        # Based on lengthy Stack Overflow answer by user "Maggyero" posted on
        # 2018-06-02 at https://stackoverflow.com/a/50661674/743730
        eq = self.__eq__(other)
        if eq is not NotImplemented:
            return not eq
        return NotImplemented


    def __lt__(self, other):
        return self.name() < other.name()


    def __gt__(self, other):
        if isinstance(other, type(self)):
            return other.name() < self.name()
        return NotImplemented


    def __le__(self, other):
        if isinstance(other, type(self)):
            return not other.name() < self.name()
        return NotImplemented


    def __ge__(self, other):
        if isinstance(other, type(self)):
            return not self.name() < other.name()
        return NotImplemented


    @property
    @classmethod
    @abstractmethod
    def name(cls):
        '''Returns the canonical internal name for this method.'''
        pass


    @property
    @classmethod
    @abstractmethod
    def description(cls):
        '''Returns a description what this method does.'''
        pass


    @property
    @classmethod
    @abstractmethod
    def file_extension(cls):
        '''Returns the file extension to which this method is limited
        A value of None means it is not limited to any particular file type.
        '''
        pass


    @abstractmethod
    def write_link(self, file, uri):
        '''Write the link into the file.'''
        pass
