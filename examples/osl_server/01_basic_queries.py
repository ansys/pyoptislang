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

from ansys.optislang.core import Optislang
import ansys.optislang.core.examples as examples

#########################################################
# Create optiSLang instance
# ~~~~~~~~~~~~~~~~~~~~~~~~~
# Create the optiSLang instance.

example_path = examples.get_files("ten_bar_truss")[1][0]
tmp_dir = Path(tempfile.mkdtemp())
file_path = tmp_dir / "evaluate_design_example.opf"

osl = Optislang(project_path=example_path)
osl.save_as(file_path)

#########################################################
# Get optiSLang server connection info
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Print osl server host and port.
print(f"Server host/address: {osl.get_osl_server().get_host()}")
print(f"Server port: {osl.get_osl_server().get_port()}")

#########################################################
# Get optiSLang info and optiSLang server info
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Print optiSLang and optiSLang server info.
print(f"Server info: {osl.get_osl_server().get_server_info()}")
print(f"optiSLang version: {osl.get_osl_server().get_osl_version()}")
print(f"optiSLang version string: {osl.get_osl_server().get_osl_version_string()}")

#########################################################
# Get basic project info
# ~~~~~~~~~~~~~~~~~~~~~~
# Query basic server/project info.

print(f"Basic project info: {osl.get_osl_server().get_basic_project_info()}")
print(f"Project description: {osl.get_osl_server().get_project_description()}")
print(f"Project file location: {osl.get_osl_server().get_project_location()}")
print(f"Project working directory: {osl.get_osl_server().get_working_dir()}")
print(f"Project name: {osl.get_osl_server().get_project_name()}")
print(f"Project (run) status: {osl.get_osl_server().get_project_status()}")
print(f"Full project tree: {osl.get_osl_server().get_full_project_tree()}")

#########################################################
# Stop and cancel project
# ~~~~~~~~~~~~~~~~~~~~~~~
# Stop and cancel the project.

osl.dispose()
