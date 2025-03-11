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

"""Find a system named "Sensitivity" and change some of its settings."""
# (c) 2021 ANSYS, Inc. Unauthorized use, distribution, or duplication is prohibited.
#
# Python example
#
# Find a system named "Sensitivity" and change some of its settings

from dynardo_py_algorithms import DOETYPES
import py_doe_settings

sens = actors.SensitivityActor("Sensitivity")
add_actor(sens)
sensitivity_system = find_actor("Sensitivity")

new_settings = sensitivity_system.algorithm_settings
new_settings.num_discretization = 200
new_settings.sampling_method = DOETYPES.PLAINMONTECARLO

sensitivity_system.algorithm_settings = new_settings
