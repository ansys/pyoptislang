# Copyright (C) 2022 - 2026 ANSYS, Inc. and/or its affiliates.
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

import pytest

from ansys.optislang.core.node_types import AddinType, NodeType
from ansys.optislang.core.settings.enums import ReadMode
import ansys.optislang.core.settings.primitives as primitives
from ansys.optislang.core.tcp.nodes import TcpNodeProxy


class _MockedServer:
    def __init__(self):
        self.calls = []

    def set_actor_property(self, actor_uid, name, value):
        self.calls.append({"actor_uid": actor_uid, "name": name, "value": value})


def test_primitive_call_with_initial_value():
    prop = primitives.AUTO_SAVE_MODE("no_auto_save")
    assert prop.name == "AutoSaveMode"
    assert prop.value == "no_auto_save"


def test_primitive_call_then_assign_value():
    prop = primitives.READ_MODE()
    prop.value = "read_and_write_mode"
    assert prop.name == primitives.READ_MODE.name
    assert prop.value == "read_and_write_mode"
    prop.value = ReadMode.CLASSIC_REEVALUATE_MODE
    assert prop.value == ReadMode.CLASSIC_REEVALUATE_MODE.value


def test_tcp_node_set_property_accepts_setting_instance():
    server = _MockedServer()
    node = TcpNodeProxy(
        uid="test_uid",
        osl_server=server,
        type_=NodeType("Dummy", AddinType.BUILT_IN),
    )

    prop = primitives.READ_MODE("classic_reevaluate_mode")
    node.set_property(prop.name, prop)

    assert len(server.calls) == 1
    assert server.calls[0]["name"] == "ReadMode"
    assert server.calls[0]["value"] == {"value": "classic_reevaluate_mode"}


def test_tcp_node_set_property_raises_on_name_mismatch_for_setting_instance():
    server = _MockedServer()
    node = TcpNodeProxy(
        uid="dummy_uid",
        osl_server=server,
        type_=NodeType("Dummy", AddinType.BUILT_IN),
    )

    prop = primitives.READ_MODE("classic_reevaluate_mode")
    with pytest.raises(ValueError, match="Property name mismatch"):
        node.set_property("WrongName", prop)
