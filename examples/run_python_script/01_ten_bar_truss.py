"""
.. _ref_ten_bar_truss:

Ten bar truss
-------------

This example uses the ``arsm_ten_bar_truss.py`` file to create an ARSM ten bar
truss flow in batch. It then uses the ``ten_bar_modify_parameters.py`` and
``ten_bar_truss_lc2.py`` files to modify the flow. Lastly, it runs the project
and explains how you can optionally save a copy of the project to a desired
location. For more detailed information, see the individual Python files for
the ten bar truss example in the optiSLang tutorials.
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

paths1 = examples.get_files("arsm_ten_bar_truss")
paths2 = examples.get_files("ten_bar_modify_parameters")
paths3 = examples.get_files("ten_bar_truss_lc2")

osl.run_python_file(paths1[0])
osl.run_python_file(paths2[0])
osl.run_python_file(paths3[0])

#########################################################
# Run workflow
# ~~~~~~~~~~~~
# Run the workflow created by the preceding scripts.

osl.start()

#########################################################
# Optionally save project
# ~~~~~~~~~~~~~~~~~~~~~~~
# If you want to save the project to some desired location,
# uncomment and edit these lines:
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

# .. image:: ../../../_static/01_ten_bar_truss.png
#  :width: 400
#  :alt: Result of script.
#
