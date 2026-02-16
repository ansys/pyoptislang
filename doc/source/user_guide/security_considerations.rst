.. _ref_security_considerations:

========================
Security considerations
========================

This section provides information about security considerations when using PyOptiSLang.
It documents security-related decisions made during development and provides guidance
for secure usage of the library.

Overview
========

PyOptiSLang is regularly scanned for security vulnerabilities using automated tools
such as `Bandit <https://bandit.readthedocs.io/>`_ for code security analysis and
`Safety <https://pyup.io/safety/>`_ for dependency vulnerability checking. These
scans are integrated into the CI/CD pipeline to ensure continuous security monitoring.

Process management security
============================

PyOptiSLang uses the Python ``subprocess`` module to launch and manage the optiSLang
server process. This is necessary for the core functionality of the library. The
following security measures are implemented to ensure safe process management:

Subprocess usage (B404)
------------------------

**Bandit check:** ``B404`` - Import of subprocess module

**Status:** Excluded inline with ``# nosec B404`` comment

**Justification:**

The ``subprocess`` module is imported in
:py:mod:`ansys.optislang.core.osl_process` for legitimate process management purposes.
All subprocess usage in PyOptiSLang follows security best practices:

1. **Shell injection prevention**: All subprocess calls use ``shell=False`` to prevent
   shell injection attacks. Arguments are passed as lists rather than shell strings.

2. **Input validation**: The optiSLang executable path is validated to exist during
   initialization. All command-line arguments are constructed from validated internal
   state rather than user-controlled input.

3. **No arbitrary command execution**: The subprocess module is used exclusively to
   launch the optiSLang application with controlled arguments. No user input is
   directly executed as shell commands.

4. **Secure by design**: All subprocess calls include detailed security comments
   documenting why they are safe (see line 1266-1278 in ``osl_process.py``).

Inline exclusion example
-------------------------

The subprocess module import includes an inline exclusion following PyAnsys guidelines:

.. code-block:: python

    # Subprocess is required for legitimate optiSLang process management.
    # All arguments are validated and shell=False is enforced. See security audit in __start_in_python.
    import subprocess  # nosec B404

This approach is preferred over global exclusions because it:

- Documents the security justification at the point of use
- Makes code reviews easier by providing context
- Follows PyAnsys ecosystem standards for vulnerability management

Example of secure subprocess usage
-----------------------------------

The following code snippet from ``osl_process.py`` demonstrates the secure usage pattern:

.. code-block:: python

    # Security: This subprocess call is safe because:
    # 1. shell=False is explicitly set to prevent shell injection
    # 2. The executable path is validated to exist in __init__
    # 3. All arguments are constructed from validated internal state
    # 4. This is a controlled call to start the optiSLang application
    self.__process = subprocess.Popen(  # nosec B603
        args,
        env=env_vars,
        cwd=os.getcwd(),
        stderr=subprocess.PIPE if self.__log_process_stderr else subprocess.DEVNULL,
        stdout=subprocess.PIPE if self.__log_process_stdout else subprocess.DEVNULL,
        shell=False,
        creationflags=creation_flags,
    )

User security considerations
=============================

When using PyOptiSLang in your applications, consider the following security practices:

Executable path validation
---------------------------

If you specify a custom optiSLang executable path, ensure that:

- The path points to a legitimate optiSLang installation
- The executable has not been tampered with
- The directory containing the executable has appropriate access controls

Example:

.. code-block:: python

    from ansys.optislang.core import Optislang
    from pathlib import Path

    # Validate the executable exists and is from a trusted location
    trusted_executable = Path("/path/to/trusted/optislang")
    if trusted_executable.exists():
        osl = Optislang(executable=trusted_executable)

Project file handling
----------------------

When working with optiSLang project files:

- Validate project file paths to prevent path traversal attacks
- Only open project files from trusted sources
- Be cautious when sharing projects that may contain sensitive data

Environment variables
---------------------

PyOptiSLang allows passing custom environment variables to the optiSLang process.
Ensure that:

- Environment variables do not contain sensitive information unless necessary
- Custom environment variables are validated before being passed to the process

Network security
----------------

PyOptiSLang uses **secure local domain communication by default**. When you launch an
optiSLang instance without specifying a ``communication_channel``, it establishes a
local domain communication channel that:

- Only allows local communication (no network exposure)
- Restricts access to the user who started the instance
- Uses platform-specific secure mechanisms (Named Pipes on Windows, Unix Domain Sockets on Linux)

This default configuration provides the best security for most use cases.

TCP-based communication (opt-in only)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

TCP-based communication is **only enabled when explicitly requested** by setting
``communication_channel=CommunicationChannel.TCP``. When using TCP-based communication:

- Communication is **not encrypted** (no TLS by default)
- The server listens on **localhost only by default** unless ``server_address`` is explicitly set
- Setting ``server_address`` to ``"0.0.0.0"`` exposes the server to network access

**Security recommendations for TCP communication:**

- Only use TCP communication when remote access is specifically required
- Use appropriate firewall rules to restrict access to the optiSLang server
- Be aware that communication is not encrypted by default
- Never expose the server to untrusted networks without additional security measures

Example of secure local communication (default):

.. code-block:: python

    from ansys.optislang.core import Optislang

    # Default: Secure local domain communication (recommended)
    osl = Optislang()

Example of TCP communication with localhost binding:

.. code-block:: python

    from ansys.optislang.core import Optislang
    from ansys.optislang.core.communication_channels import CommunicationChannel

    # TCP communication, localhost only (more secure)
    osl = Optislang(
        communication_channel=CommunicationChannel.TCP,
        port_range=(5000, 5010),
        # Note: server_address defaults to "127.0.0.1" (localhost only)
    )

Reporting vulnerabilities
==========================

If you discover a security vulnerability in PyOptiSLang, please do not report it
through GitHub issues. Instead, refer to the `SECURITY.md <https://github.com/ansys/pyoptislang/blob/main/SECURITY.md>`_
file in the repository for instructions on how to report security issues to the
PyAnsys Core team.

Additional resources
====================

For more information about security in the PyAnsys ecosystem, see:

- `PyAnsys Developer Guide - Vulnerabilities <https://dev.docs.pyansys.com/how-to/vulnerabilities.html>`_
- `Bandit documentation <https://bandit.readthedocs.io/>`_
- `OWASP Secure Coding Practices <https://owasp.org/www-project-secure-coding-practices-quick-reference-guide/>`_
