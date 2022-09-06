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
