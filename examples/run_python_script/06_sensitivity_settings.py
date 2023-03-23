"""
.. _ref_sensitivity_settings:

Sensitivity settings
--------------------

This example creates a system named "Sensitivity". It then finds this system and uses
the ``sensitivity_settings.py`` file to change some of its settings. Lastly, it
explains how you can optionally save a copy of the project to a desired location.
For more detailed information, see the individual Python files for the oscillator
example in the optiSLang tutorials.
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
# Get path of example script and run it
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Get the path of the example script and then run it.

paths = examples.get_files("sensitivity_settings")
osl.run_python_file(paths[0])

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

# .. image:: ../../../_static/06_sensitivity_settings.png
#  :width: 300
#  :alt: Result of script.
#
