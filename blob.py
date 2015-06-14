# Copyright 2015, Nashwan Azhari.
# Licensed under the GPLv2, see LICENSE file for details.

"""
Basic Blob structure used for data manipulation.
"""

from ctypes import c_char
from ctypes import create_string_buffer
from ctypes import POINTER
from ctypes import Structure
from ctypes import cdll
from ctypes import windll
from ctypes.wintypes import DWORD

memcpy = cdll.msvcrt.memcpy
localfree = windll.kernel32.LocalFree


class Blob(Structure):
    """Basic Structure used for data manipulation.
    It is structurally identical to the native CRYPT_INTEGER_BLOB structure.

    Composed of a field holding the length of the data and a
    pointer to the start of it.
    """
    _fields_ = [("length", DWORD), ("data", POINTER(c_char))]

    def get_data(self):
        """Fetches the data from the Blob."""
        fetched = create_string_buffer(self.length)

        memcpy(fetched, self.data, self.length)

        return fetched.raw

    def free_blob(self):
        """Frees the memory allocated for the Blob's data."""
        localfree(self.data)
