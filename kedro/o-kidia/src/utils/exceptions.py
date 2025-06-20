""" Module that contains all customs exceptions.
"""


class UnexpectedFormatError(Exception):
    """Exception raised when any file (CSV, Excel, JSON,...) does not have the
    expected format."""
