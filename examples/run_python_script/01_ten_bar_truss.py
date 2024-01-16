"""
.. _ref_ten_bar_truss:

Ten bar truss
-------------

This example demonstrates how to to create an ARSM ten bar truss flow in batch mode
using optiSLang python API.

First, the ``arsm_ten_bar_truss.py`` file is used to create an ARSM ten bar
truss flow. Then the ``ten_bar_modify_parameters.py`` and
``ten_bar_truss_lc2.py`` files are used to modify the flow. Lastly, the project is
executed and a optionally the project is saved to a desired location.
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

osl = Optislang(ini_timeout=60)
print(osl)

#########################################################
# Get paths of example scripts and run them
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Get the paths of the example scripts and then run these
# scripts.

paths1 = examples.get_files("arsm_ten_bar_truss")
paths2 = examples.get_files("ten_bar_modify_parameters")
paths3 = examples.get_files("ten_bar_truss_lc2")

osl.application.project.run_python_file(paths1[0])
osl.application.project.run_python_file(paths2[0])
osl.application.project.run_python_file(paths3[0])

#########################################################
# Run workflow
# ~~~~~~~~~~~~
# Run the workflow created by the preceding scripts.

osl.application.project.start()

#########################################################
# Optionally save project
# ~~~~~~~~~~~~~~~~~~~~~~~
# If you want to save the project to some desired location,
# uncomment and edit these lines:
#
# .. code:: python
#
#   path = r'<insert-desired-location>'
#   osl.application.save_as(os.path.join(path, "test_project.opf"))
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
# .. image:: ../../_static/01_ten_bar_truss.png
#  :width: 400
#  :alt: Result of script.
#
