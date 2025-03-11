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

from enum import Enum
from socket import getaddrinfo, gethostname

import pytest

from ansys.optislang.core import utils


@pytest.fixture
def localhost_addresses():
    """Get addresses of the local machine excluding loopback addresses."""
    addresses = []
    for _, _, _, _, sockaddr in getaddrinfo(gethostname(), None):
        addresses.append(sockaddr[0])
    return addresses


@pytest.fixture
def loopback_addresses():
    """Get loopback addresses."""
    return ["127.0.0.0", "127.0.0.1", "127.255.255.255", "::1", "localhost"]


def test_enum_from_str():
    class MyEnum(Enum):
        ONE = 0
        TWO = 1

    with pytest.raises(TypeError):
        utils.enum_from_str(123, MyEnum)
        utils.enum_from_str("ONE", list)

    with pytest.raises(ValueError):
        utils.enum_from_str("THREE", MyEnum)

    assert utils.enum_from_str("one", MyEnum) == MyEnum.ONE
    assert utils.enum_from_str("ONE", MyEnum) == MyEnum.ONE
    assert utils.enum_from_str("ONX", MyEnum, ["X", "E"]) == MyEnum.ONE


def test_get_localhost_addresses(localhost_addresses):
    for address in utils.get_localhost_addresses():
        assert address in localhost_addresses


def test_is_localhost(loopback_addresses, localhost_addresses):
    random_addresses = [
        "192.168.101.1",
        "10.0.10.1",
        "130.10.20.1",
        "2001:0db8:85a3:0000:0000:8a2e:0370:7334",
        "fe80::1ff:fe23:4567:890a%3",
    ]

    for loopback_address in loopback_addresses:
        assert utils.is_localhost(loopback_address) == True

    for localhost_address in localhost_addresses:
        assert utils.is_localhost(localhost_address) == True

    for random_address in random_addresses:
        assert utils.is_localhost(random_address) == (random_address in localhost_address)
