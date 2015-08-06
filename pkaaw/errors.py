from __future__ import print_function, unicode_literals


class PKAAWException(Exception):
    """Base Exception class for errors."""
    def __init__(self, message):
        self.message = message

    def __str__(self):
        """Rerturn the message of the error"""
        return self.message


class ActiveSessionRequired(PKAAWException):
    """Indicates that an authorized session is required.

    This exception is raised when a Coach or Student is created without
    an authorized session being initialized first

    """

    def __init__(self, message=None):
        if not message:
            message = 'This class requires an initialized KhanSession().'
        super(ActiveSessionRequired, self).__init__(message)
