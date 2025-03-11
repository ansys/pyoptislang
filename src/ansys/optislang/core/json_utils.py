# Copyright (C) 2022 - 2025 ANSYS, Inc. and/or its affiliates.
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

"""Json utilities module."""

from typing import Any


def _get_enum_value(enum_value: Any, default_value: str = "", throw_on_error: bool = True) -> str:
    """Get value of an enum encoded in oSL Json.

    Parameters
    ----------
    enum_value : Any
        The enum encoded in oSL Json. Can be either a plain string
        or a dict in the format ``{ "enum" : [], "value" : "" }``.
    default_value : str
        The default value if not present or convertible.

    Returns
    -------
    str
        The decoded enum value. If not present or convertible and throw_on_error is False,
        ``default_value`` is returned, otherwise, an exception it raised.
    Raises
    ------
    TypeError
        Raised when the decoded enum_value is not a string.
    ValueError
        Raised when the value for the ``string`` is invalid.
    """
    if isinstance(enum_value, dict):
        value = enum_value.get("value")
        if value is None:
            if throw_on_error:
                raise ValueError(
                    f"Cannot decode {enum_value} as enum: Doesn't contain the 'value' entry."
                )
            else:
                return default_value
        elif isinstance(value, str):
            return value
        else:
            if throw_on_error:
                raise TypeError(
                    f"Cannot decode {enum_value} as enum: 'value' entry is not of type str."
                )
            else:
                return default_value
    elif isinstance(enum_value, str):
        return enum_value
    else:
        if throw_on_error:
            raise TypeError(f"Cannot decode {enum_value} as enum: str or dict expected.")
        else:
            return default_value
