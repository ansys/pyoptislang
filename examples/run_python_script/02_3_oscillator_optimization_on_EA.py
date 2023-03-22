"""
.. _ref_oscillator_optimization_on_EA:

Oscillator optimization using EA flow
-------------------------------------

This example uses the ``oscillator_optimization_ea.py`` file to create and
run a direct optimization for an oscillator using the EA (Evolutionary
Algorithm) optimizer. It then explains how you can optionally save a copy
of the project to a desired location. For more detailed information, see
the individual Python files for the oscillator example in the optiSLang
tutorials.
"""

#########################################################
# Perform required imports
# ~~~~~~~~~~~~~~~~~~~~~~~~
# Perform the required imports.

from ansys.optislang.core import Optislang
import ansys.optislang.core.examples as examples

#########################################################
# Create optiSLang instance
# ~~~~~~~~~~~~~~~~~~~~~~~~~
# Create the optiSLang instance.

osl = Optislang()
print(osl)

#########################################################
# Get paths of example scripts and run them
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Get the paths of the example scripts and then run them.

paths = examples.get_files("oscillator_optimization_ea")
osl.run_python_file(paths[0])

#########################################################
# Run workflow
# ~~~~~~~~~~~~
# Run the workflow created by the preceding scripts.

osl.start()

#########################################################
# Optionally save project
# ~~~~~~~~~~~~~~~~~~~~~~~
# If you want to save the project to some desired
# location, uncomment and edit these lines:
#
# .. code:: python
#
#   path = r'<insert-desired-location>'
#   osl.save_as(os.path.join(path, "test_project.opf"))
#
#########################################################
# Stop and cancel project
# ~~~~~~~~~~~~~~~~~~~~~~~
# Stop and cancel the project.

osl.dispose()

#########################################################
# View generated workflow
# ~~~~~~~~~~~~~~~~~~~~~~~
# This image shows the generated workflow.
#
# .. image:: ../../../_static/02_3_optimization_on_EA.png
#  :width: 400
#  :alt: Result of script.
#
#########################################################
