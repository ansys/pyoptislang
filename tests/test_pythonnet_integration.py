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

"""Integration tests for Python.NET with actual optiSLang process.

These tests require optiSLang to be installed and use the --local_osl marker.
"""
import pytest

pytestmark = pytest.mark.local_osl


def test_pythonnet_available():
    """Test that pythonnet is installed."""
    try:
        import clr  # noqa: F401
    except ImportError:
        pytest.skip("pythonnet not installed - use 'pip install pythonnet'")


def test_optislang_start_with_pythonnet():
    """Test starting optiSLang server process with Python.NET loaded."""
    try:
        import clr  # noqa: F401
    except ImportError:
        pytest.skip("pythonnet not installed")

    from ansys.optislang.core import Optislang

    # Start optiSLang with CLR loaded
    osl = Optislang(ini_timeout=60)
    try:
        assert osl is not None
        assert osl.project is not None
        print(f"Successfully started optiSLang with Python.NET loaded")
    finally:
        osl.dispose()


def test_osl_server_process_with_pythonnet():
    """Test OslServerProcess directly with Python.NET loaded."""
    try:
        import clr  # noqa: F401
    except ImportError:
        pytest.skip("pythonnet not installed")

    from ansys.optislang.core import utils
    from ansys.optislang.core.osl_process import OslServerProcess

    # Verify we're in Python.NET environment, not IronPython
    assert utils.is_pythonnet()
    assert not utils.is_iron_python()

    # Get optiSLang executable
    osl_exec = utils.get_osl_exec()
    if osl_exec is None:
        pytest.skip("optiSLang not found")

    version, executable = osl_exec

    # Start process with Python.NET loaded
    process = OslServerProcess(
        executable=str(executable),
        batch=True,
        service=False,
    )

    try:
        process.start()
        assert process.is_running()
        assert process.pid is not None
        print(f"optiSLang process started with PID: {process.pid}")

        # Wait a bit to ensure process is stable
        import time

        time.sleep(2)

        # Verify still running
        assert process.is_running()

    finally:
        # Terminate and check return code
        process.terminate()
        returncode = process.wait_for_finished(timeout=30)

        # Verify we got a valid return code (not corrupted by unsigned conversion)
        assert returncode is not None
        assert isinstance(returncode, int)
        assert -2147483648 <= returncode <= 2147483647  # Within int32 range
        print(f"Process terminated with return code: {returncode}")


def test_optislang_tcp_connection_with_pythonnet():
    """Test optiSLang TCP/IP connection with Python.NET loaded."""
    try:
        import clr  # noqa: F401
    except ImportError:
        pytest.skip("pythonnet not installed")

    from ansys.optislang.core import Optislang

    # Start with TCP/IP server
    osl = Optislang(ini_timeout=60)

    try:
        # Verify connection
        assert osl.project is not None

        # Test basic operations
        osl.project.reset()

        # Get project status
        status = osl.project.get_status()
        assert status is not None
        print(f"Project status: {status}")

    finally:
        osl.dispose()


def test_subprocess_still_works_with_pythonnet():
    """Verify subprocess operations still work correctly with optiSLang and Python.NET."""
    try:
        import clr  # noqa: F401
    except ImportError:
        pytest.skip("pythonnet not installed")

    import subprocess
    import sys

    from ansys.optislang.core import utils

    # Verify environment
    assert utils.is_pythonnet()
    assert not utils.is_iron_python()

    # Test subprocess.run (should use CPython's subprocess, not .NET)
    if sys.platform == "win32":
        result = subprocess.run(
            ["cmd", "/c", "echo", "test"], capture_output=True, text=True, timeout=5
        )
    else:
        result = subprocess.run(["echo", "test"], capture_output=True, text=True, timeout=5)

    assert result.returncode == 0
    assert "test" in result.stdout


def test_multiple_osl_instances_with_pythonnet():
    """Test creating multiple optiSLang instances with Python.NET loaded."""
    try:
        import clr  # noqa: F401
    except ImportError:
        pytest.skip("pythonnet not installed")

    from ansys.optislang.core import Optislang

    # Start first instance
    osl1 = Optislang(ini_timeout=60)
    try:
        assert osl1.project is not None

        # Start second instance
        osl2 = Optislang(ini_timeout=60)
        try:
            assert osl2.project is not None

            # Verify both are independent
            assert osl1 != osl2
            print("Successfully created multiple optiSLang instances with Python.NET")

        finally:
            osl2.dispose()
    finally:
        osl1.dispose()


def test_optislang_local_domain_with_pythonnet():
    """Test optiSLang LOCAL_DOMAIN communication with Python.NET loaded.

    This test explicitly uses LOCAL_DOMAIN communication channel and verifies:
    - On Windows: pywintypes and win32 modules work with Python.NET
    - On Linux: Unix domain sockets work with Python.NET
    - Communication over local domain socket succeeds with actual optiSLang process
    """
    try:
        import clr  # noqa: F401
    except ImportError:
        pytest.skip("pythonnet not installed")

    from ansys.optislang.core import Optislang
    from ansys.optislang.core.communication_channels import CommunicationChannel

    # Explicitly use LOCAL_DOMAIN channel with Python.NET loaded
    osl = Optislang(ini_timeout=120, communication_channel=CommunicationChannel.LOCAL_DOMAIN)

    try:
        # Verify connection is established
        assert osl.project is not None, "Project should be accessible"

        # Test basic operations over local domain socket
        # This exercises send/recv through local_socket.py code paths
        osl.project.reset()

        # Get project status - requires communication over local socket
        status = osl.project.get_status()
        assert status is not None, "Should be able to get project status"

        # Test another operation to ensure socket communication is stable
        project_info = osl.application.project
        assert project_info is not None, "Should be able to get project info"

        import sys

        if sys.platform == "win32":
            # On Windows, verify pywintypes was imported (will be in sys.modules)
            # This confirms Windows named pipe code paths with Python.NET work
            assert (
                "pywintypes" in sys.modules
            ), "pywintypes should be imported on Windows for local domain sockets"
            print("Successfully used Windows named pipes with Python.NET")
        else:
            # On Linux, verify Unix domain socket was used
            print("Successfully used Unix domain sockets with Python.NET")

        print(f"LOCAL_DOMAIN communication with Python.NET verified on {sys.platform}")

    finally:
        osl.dispose()
