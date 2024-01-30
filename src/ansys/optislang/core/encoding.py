# Copyright (C) 2022 - 2024 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Contains utility functions for encoding and decoding text."""

import sys

from ansys.optislang.core import IRON_PYTHON, PY3

defenc = sys.getdefaultencoding()

if PY3:
    text_type = str
    binary_type = bytes
else:
    if defenc == "ascii":
        defenc = "utf-8"
    text_type = unicode
    binary_type = str

string_types = (binary_type,)


def safe_decode(s):
    """Safely decodes a binary_type to text_type."""
    if isinstance(s, text_type):
        return s
    elif isinstance(s, string_types):
        return s.decode(defenc, "surrogateescape")
    elif s is not None:
        raise TypeError("Expected bytes or text, but got %r" % (s,))


def to_ascii_safe(text: str) -> str:
    """Safely converts text encoding to ASCII standard.

    Conversion is performed ignoring the unencodable unicode characters.

    Parameters
    ----------
    text : str
        String which is supposed to be encoded to ASCII standard.

    Returns
    -------
    str
        String encoded in ASCII standard.
    """
    return text.encode("ascii", "ignore").decode("ascii")


def force_bytes(text: str, encoding="ascii") -> bytes:
    """Encode data to bytes ignoring all errors.

    Special characters are ignored.

    Parameters
    ----------
    text : str
        String which is supposed to be encoded.
    encoding :
        String encoding.

    Returns
    -------
    bytes
        An encoded version of the string as a bytes object.
    """
    if IRON_PYTHON:
        return binary_type(text.encode(encoding, "ignore"), encoding, "ignore")
    else:
        return text.encode(encoding, "ignore")


def force_text(data: bytes, encoding="utf-8") -> str:
    """Decode bytes to text ignoring all errors.

    Special characters are ignored.

    Parameters
    ----------
    data : bytes
        Bytes which is supposed to be decoded.
    encoding :
        The encoding with which to decode the bytes.

    Returns
    -------
    str
        Decoded string.
    """
    if isinstance(data, string_types):
        return data.decode(encoding, errors="ignore")

    if PY3:
        return text_type(data, encoding)
    else:
        return text_type(data)
