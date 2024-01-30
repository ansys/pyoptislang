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

"""Create, configure and insert EAO."""
# (c) 2021 ANSYS, Inc. Unauthorized use, distribution, or duplication is prohibited.
#
# Create, configure and insert an Evolutionary Algorithm Optimizer into
# the scenery.

import PyNOA

# Construct a n settings object
ea_settings = PyNOA.NOASettings()

# Configure some global settings
ea_settings.set_defaults()
ea_settings.set_start_pop_size(45)
ea_settings.set_min_gen(10)

# Set and configure the first adaption method
ea_settings.set_adaption_method(PyNOA.Multipoint)
ea_settings.set_number_of_crosspoints(3)
ea_settings.set_crossover_probability(0.3)
ea_settings.set_distribution_parameter(3)

# For hybrid optimization, append another adaption method,
# then use the same functions as before to configure the
# second adaption.
ea_settings.set_hybrid(True)
ea_settings.append_adaption_method(PyNOA.Multipoint)
ea_settings.set_number_of_crosspoints(2)
ea_settings.set_crossover_probability(0.2)
ea_settings.set_distribution_parameter(2)

# Note: to change the settings for the first adaption method afterwards, you
# have to start again with the routine beginning on line 14:
# 1. set the first method and configure it
# 2. append the second method and configure it


# Create the actor
ea = actors.EAActor("My_EA")
# Apply the settings
ea.optimizer_settings = ea_settings
# Add the actor to the scenery
add_actor(ea)
