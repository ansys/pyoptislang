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
