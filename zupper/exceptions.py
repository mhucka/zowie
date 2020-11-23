'''
exceptions.py: exceptions defined by Zupper

Authors
-------

Michael Hucka <mhucka@caltech.edu> -- Caltech Library

Copyright
---------

Copyright (c) 2020 by Michael Hucka and the California Institute of Technology.
This code is open-source software released under a 3-clause BSD license.
Please see the file "LICENSE" for more information.
'''


# Base class.
# .............................................................................
# The base class makes it possible to use a single test to distinguish between
# exceptions generated by Zupper and exceptions generated by something else.

class ZupperException(Exception):
    '''Base class for Zupper exceptions.'''
    pass


# Exception classes.
# .............................................................................

class CannotProceed(ZupperException):
    '''A recognizable condition caused an early exit from the program.'''
    pass

class UserCancelled(ZupperException):
    '''The user elected to cancel/quit the program.'''
    pass

class NetworkFailure(ZupperException):
    '''Unrecoverable problem involving network operations.'''
    pass

class NoContent(ZupperException):
    '''No content found at the given location.'''
    pass

class CorruptedContent(ZupperException):
    '''Content corruption has been detected.'''
    pass

class AuthFailure(ZupperException):
    '''Problem obtaining or using authentication credentials.'''
    pass

class ServiceFailure(ZupperException):
    '''Unrecoverable problem involving a remote service.'''
    pass

class RateLimitExceeded(ZupperException):
    '''The service flagged reports that its rate limits have been exceeded.'''
    pass

class InternalError(ZupperException):
    '''Unrecoverable problem involving eprints2bags itself.'''
    pass