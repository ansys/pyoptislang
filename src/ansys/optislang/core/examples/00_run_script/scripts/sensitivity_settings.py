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
