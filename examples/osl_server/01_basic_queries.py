"""
.. _ref_osl_server_basic_queries:

Basic server queries
--------------------

This example demonstrates how to use PyOptiSLang to perform basic
queries/commands on the optiSLang server using the explicit API.

"""

#########################################################
# Perform required imports
# ~~~~~~~~~~~~~~~~~~~~~~~~
# Perform the required imports.

from pathlib import Path
import tempfile
from typing import TYPE_CHECKING

from ansys.optislang.core import Optislang
import ansys.optislang.core.examples as examples

if TYPE_CHECKING:
    from ansys.optislang.core.tcp.osl_server import TcpOslServer

#########################################################
# Create optiSLang instance
# ~~~~~~~~~~~~~~~~~~~~~~~~~
# Create the optiSLang instance.

example_path = examples.get_files("ten_bar_truss")[1][0]
tmp_dir = Path(tempfile.mkdtemp())
file_path = tmp_dir / "evaluate_design_example.opf"

osl = Optislang(project_path=example_path)
osl.application.save_as(file_path)
osl_server: TcpOslServer = osl.osl_server

#########################################################
# Get optiSLang server connection info
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Print osl server host and port.
print(f"Server host/address: {osl_server.host}")
print(f"Server port: {osl_server.port}")

#########################################################
# Get optiSLang info and optiSLang server info
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Print optiSLang and optiSLang server info.
print(f"Server info: {osl_server.get_server_info()}")

#########################################################
# Get basic project info
# ~~~~~~~~~~~~~~~~~~~~~~
# Query basic server/project info.

print(f"Basic project info: {osl_server.get_basic_project_info()}")
print(f"Full project tree: {osl_server.get_full_project_tree()}")

#########################################################
# Stop and cancel project
# ~~~~~~~~~~~~~~~~~~~~~~~
# Stop and cancel the project.

osl.dispose()
