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

"""Modify parameters."""
###############################################################################
# (c) 2021 ANSYS, Inc. Unauthorized use, distribution, or duplication is prohibited.
#
# modify flow created by arsm_ten_bar_truss.py
# set lowerbounds of a parameter
# run following command from command line:
# optislang ten_bar_arsm.opf --batch --python ten_bar_modify_parameters.py --no-run

# or choose this file after selecting "Run script file" from Python console's
# context menu
###############################################################################
from py_os_design import *

# import needed modules
from py_os_parameter import *

### ARSM node ###
# get the ARSM node
arsm = find_actor("ARSM")

### Parameter modification ###
# get the parameter manager of ARSM node
params = arsm.parameter_manager
# e.g. SetLowerBound to 5.0 of a parameter
params.set_bounds("area01", PyOSDesignEntry(5.0), PyOSDesignEntry(15.0))
# set parameter manager at ARSM node
arsm.parameter_manager = params
