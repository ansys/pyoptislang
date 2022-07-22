"""Contains utility functions for encoding and decoding text."""

import sys

from ansys.optislang.core import PY3

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
        return s.decode(defenc, "ignore")
    elif s is not None:
        raise TypeError("Expected bytes or text, but got %r" % (s,))


def safe_encode_to_ascii(text: str) -> str:
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
