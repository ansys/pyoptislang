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
DYNARDO example.

Damped oscillator

Undamped eigenfrequency: omega_0 = sqrt(k/m)
Damped eigenfrequency:     omega = sqrt(1-D^2)*omega_0
Response:                   x(t) = exp(-D*omega_0*t)*sqrt(2*Ekin/m)/omega*sin(omega*t)

Minimize maximum amplitude after 5 seconds
Maximum eigenfrequencies as constraint: omega <= 8 1/s

0.1 kg <= m <= 5.0 kg
10 N/m <= k <= 50 N/m
D = 0.02
Ekin = 10 Nm

For background information see ../doc/oszillator.pdf
"""
from math import *

# Check if Python is called outside optiSLang
if not "OSL_REGULAR_EXECUTION" in locals():
    OSL_REGULAR_EXECUTION = False

# values to default if not existing yet
if not OSL_REGULAR_EXECUTION:  # test run mode
    m = 1.00000000
    k = 20.00000000
    D = 0.02000000
    Ekin = 10.00000000

# scalar values
v0 = sqrt(2 * Ekin / m)
omega0 = sqrt(k / m)
omega_damped = omega0 * sqrt(1 - D * D)

# approximate maximum amplitude from envelope
x_max_env = exp(-5 * D * omega0) * v0 / omega_damped
numsteps = 100


# time signal
def CalcDisplacement(_t):
    """Calculate displacement."""
    sin_value = sin(_t * omega_damped)
    envelope = exp(-_t * D * omega0) * v0 / omega_damped
    return sin_value * envelope


def CalcIndicator(_t, _x):
    """Calculate indicator."""
    if _t > 5:
        return abs(_x)
    else:
        return 0


time = range(0, numsteps)
time = [10.0 * t / (numsteps - 1) for t in time]
x_values = [CalcDisplacement(t) for t in time]


# extract maximum amplitude from time signal
x_max = max([CalcIndicator(t, x) for t, x in zip(time, x_values)])

print("omega_damped: " + str(omega_damped))
print("x_max: " + str(x_max))

try:
    from pyvariant import List2VariantVector

    time = List2VariantVector(time)
    x_values = List2VariantVector(x_values)
except:
    print("Did not export result to optiSLang")
