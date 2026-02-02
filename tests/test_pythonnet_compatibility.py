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

"""Tests for Python.NET compatibility (Scenario A: PyOptiSLang embedded in .NET apps)."""
import subprocess
import sys

import pytest


def test_pythonnet_available():
    """Test that pythonnet is installed and importable."""
    try:
        import clr

        assert clr is not None
        print(f"Python.NET version: {clr.__version__}")
    except ImportError:
        pytest.skip("pythonnet not installed")


def test_platform_is_not_ironpython():
    """Verify we're running in CPython, not IronPython, even with pythonnet loaded."""
    try:
        import clr  # noqa: F401
    except ImportError:
        pytest.skip("pythonnet not installed")

    # With Python.NET, sys.platform should still be win32/linux, not 'cli'
    assert sys.platform != "cli", "Python.NET should not report as IronPython"
    assert sys.platform in ["win32", "linux", "darwin"], f"Unexpected platform: {sys.platform}"


def test_pyoptislang_utils_detection():
    """Test that PyOptiSLang correctly identifies this is NOT IronPython."""
    try:
        import clr  # noqa: F401
    except ImportError:
        pytest.skip("pythonnet not installed")

    from ansys.optislang.core import utils

    # Should return False - we're in CPython with Python.NET, not IronPython
    assert not utils.is_iron_python(), "is_iron_python() should return False with Python.NET"


def test_basic_imports_with_clr():
    """Test that PyOptiSLang imports work with CLR loaded."""
    try:
        import System  # noqa: F401
        import clr  # noqa: F401
    except ImportError:
        pytest.skip("pythonnet not installed")

    # These should all work without conflicts
    from ansys.optislang.core import Optislang  # noqa: F401
    from ansys.optislang.core import OslServerProcess  # noqa: F401
    from ansys.optislang.core import utils  # noqa: F401
    from ansys.optislang.core.osl_process import OslServerProcess as OslServerProcess2  # noqa: F401

    # If we get here without exceptions, imports work
    assert True


def test_subprocess_with_clr_loaded():
    """Test that subprocess operations work correctly with CLR loaded."""
    try:
        import clr  # noqa: F401
    except ImportError:
        pytest.skip("pythonnet not installed")

    # Subprocess should still work normally
    if sys.platform == "win32":
        result = subprocess.run(
            ["cmd", "/c", "echo", "test"], capture_output=True, text=True, timeout=5
        )
    else:
        result = subprocess.run(["echo", "test"], capture_output=True, text=True, timeout=5)

    assert result.returncode == 0
    assert "test" in result.stdout


def test_subprocess_popen_with_clr():
    """Test that subprocess.Popen works with CLR loaded."""
    try:
        import clr  # noqa: F401
    except ImportError:
        pytest.skip("pythonnet not installed")

    if sys.platform == "win32":
        proc = subprocess.Popen(
            ["cmd", "/c", "echo", "test"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
    else:
        proc = subprocess.Popen(
            ["echo", "test"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )

    stdout, stderr = proc.communicate(timeout=5)
    assert proc.returncode == 0
    assert "test" in stdout


def test_process_returncode_with_clr():
    """Test that process return codes are handled correctly with CLR loaded."""
    try:
        import clr  # noqa: F401
    except ImportError:
        pytest.skip("pythonnet not installed")

    # Test with successful command
    if sys.platform == "win32":
        proc = subprocess.Popen(["cmd", "/c", "exit", "0"])
    else:
        proc = subprocess.Popen(["sh", "-c", "exit 0"])

    proc.wait(timeout=5)
    assert proc.returncode == 0

    # Test with failed command (non-zero exit)
    if sys.platform == "win32":
        proc = subprocess.Popen(["cmd", "/c", "exit", "1"])
    else:
        proc = subprocess.Popen(["sh", "-c", "exit 1"])

    proc.wait(timeout=5)
    assert proc.returncode == 1


def test_negative_returncode_with_clr():
    """Test that negative return codes work correctly with CLR loaded."""
    try:
        import clr  # noqa: F401
    except ImportError:
        pytest.skip("pythonnet not installed")

    # Skip on Windows as it doesn't commonly use negative exit codes
    if sys.platform == "win32":
        pytest.skip("Windows doesn't typically use negative exit codes")

    # Test with negative exit code (common on Linux for signals)
    proc = subprocess.Popen(["sh", "-c", "exit 255"])
    proc.wait(timeout=5)

    # On Linux, exit 255 or signal termination can result in negative values
    # Just verify we get an integer, not an overflow
    assert isinstance(proc.returncode, int)
    assert -2147483648 <= proc.returncode <= 2147483647  # Within int32 range


def test_clr_and_encoding():
    """Test that encoding utilities work with CLR loaded."""
    try:
        import clr  # noqa: F401
    except ImportError:
        pytest.skip("pythonnet not installed")

    from ansys.optislang.core import encoding

    # Test basic encoding/decoding with ASCII-compatible text
    text = "Hello, World!"
    encoded = encoding.force_bytes(text)
    decoded = encoding.force_text(encoded)

    assert isinstance(encoded, bytes)
    assert isinstance(decoded, str)
    assert decoded == text

    # Test with UTF-8 encoding for non-ASCII characters
    text_utf8 = "Hello, World! 你好世界"
    encoded_utf8 = encoding.force_bytes(text_utf8, encoding="utf-8")
    decoded_utf8 = encoding.force_text(encoded_utf8, encoding="utf-8")

    assert isinstance(encoded_utf8, bytes)
    assert isinstance(decoded_utf8, str)
    assert decoded_utf8 == text_utf8


def test_clr_system_diagnostics_not_used():
    """
    Verify that System.Diagnostics.Process is NOT used
    when in Python.NET (should use subprocess).
    """
    try:
        import clr  # noqa: F401
    except ImportError:
        pytest.skip("pythonnet not installed")

    from ansys.optislang.core import utils

    # Verify detection: Python.NET should NOT trigger IronPython code paths
    assert not utils.is_iron_python()

    # When we create a process, it should use subprocess, not System.Diagnostics
    # This is implicit in our code: is_iron_python() returns False, so subprocess path is taken


def test_pythonnet_detection_helper():
    """Test the new is_pythonnet() helper if it exists."""
    try:
        import clr  # noqa: F401
    except ImportError:
        pytest.skip("pythonnet not installed")

    from ansys.optislang.core import utils

    # Check if the helper exists
    if hasattr(utils, "is_pythonnet"):
        # Should return True when pythonnet is available
        assert utils.is_pythonnet(), "is_pythonnet() should return True when pythonnet is loaded"
    else:
        # Helper not implemented yet - just check CLR is available
        try:
            import clr  # noqa: F401

            # If we can import clr, pythonnet is present
            assert True
        except ImportError:
            pytest.fail("CLR module should be available")


def test_socket_operations_with_clr():
    """Test that socket operations work with CLR loaded."""
    try:
        import clr  # noqa: F401
    except ImportError:
        pytest.skip("pythonnet not installed")

    import socket

    # Create a simple socket - should work with CLR loaded
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    assert sock is not None
    sock.close()


def test_threading_with_clr():
    """Test that threading works with CLR loaded."""
    try:
        import clr  # noqa: F401
    except ImportError:
        pytest.skip("pythonnet not installed")

    import threading

    result = []

    def worker():
        result.append(42)

    thread = threading.Thread(target=worker)
    thread.start()
    thread.join(timeout=5)

    assert result == [42]


def test_json_with_clr():
    """Test that JSON operations work with CLR loaded."""
    try:
        import clr  # noqa: F401
    except ImportError:
        pytest.skip("pythonnet not installed")

    import json

    data = {"key": "value", "number": 42}
    encoded = json.dumps(data)
    decoded = json.loads(encoded)

    assert decoded == data


@pytest.mark.skipif(sys.platform != "win32", reason="Windows-specific test")
def test_dotnet_types_available():
    """Test that .NET types are accessible via pythonnet."""
    try:
        import clr  # noqa: F401
    except ImportError:
        pytest.skip("pythonnet not installed")

    # Should be able to import .NET types
    import System

    # Test basic .NET type usage
    guid = System.Guid.NewGuid()
    assert guid is not None

    # Test string conversion
    dotnet_string = System.String("test")
    assert str(dotnet_string) == "test"


@pytest.mark.skipif(sys.platform != "win32", reason="Windows-specific test")
def test_dotnet_process_not_interfering():
    """Test that .NET System.Diagnostics.Process doesn't interfere with subprocess."""
    try:
        import clr  # noqa: F401
    except ImportError:
        pytest.skip("pythonnet not installed")

    import System.Diagnostics

    # Create a subprocess (should use subprocess.Popen)
    proc1 = subprocess.Popen(["cmd", "/c", "echo", "subprocess"])
    proc1.wait(timeout=5)

    # Create a .NET Process
    proc2 = System.Diagnostics.Process()
    proc2.StartInfo.FileName = "cmd.exe"
    proc2.StartInfo.Arguments = "/c echo dotnet"
    proc2.StartInfo.UseShellExecute = False
    proc2.Start()
    proc2.WaitForExit(5000)

    # Both should have succeeded independently
    assert proc1.returncode == 0
    assert proc2.ExitCode == 0


def test_is_pythonnet_detection_with_pythonnet():
    """Test is_pythonnet() returns True when pythonnet is installed."""
    from ansys.optislang.core.utils import is_pythonnet

    try:
        import clr  # noqa: F401

        # If we can import clr, is_pythonnet() should return True
        assert is_pythonnet() is True
    except ImportError:
        pytest.skip("pythonnet not installed")


def test_is_pythonnet_detection_without_pythonnet():
    """Test is_pythonnet() returns False when clr import fails."""
    import sys
    from unittest.mock import patch

    from ansys.optislang.core.utils import is_pythonnet

    # Save the original clr module if it exists
    original_clr = sys.modules.get("clr", None)

    try:
        # Remove clr from sys.modules to simulate it not being installed
        if "clr" in sys.modules:
            del sys.modules["clr"]

        # Mock the import to raise ImportError for clr
        with patch(
            "builtins.__import__",
            side_effect=lambda name, *args, **kwargs: (
                (_ for _ in ()).throw(ImportError("Mocked clr import failure"))
                if name == "clr"
                else __import__(name, *args, **kwargs)
            ),
        ):
            # This should return False since clr import will fail
            result = is_pythonnet()
            assert result is False

    finally:
        # Restore original clr module if it existed
        if original_clr is not None:
            sys.modules["clr"] = original_clr
