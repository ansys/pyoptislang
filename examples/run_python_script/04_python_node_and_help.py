"""
.. _ref_python_node_and_help:

Python node and help
--------------------

This example uses the ``python_node.py`` file to create a Python2 node
and then adds some source code, adds and removes parameters and responses,
and adds internal variables. It then uses the ``python_help.py`` file to
print which nodes are available in the Python console. Lastly, it explains
how you can optionally save a copy of the project to a desired location.
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
# Get paths of example scripts and run them
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Get the paths of the example scripts and then run them.

paths1 = examples.get_files("python_node")
paths2 = examples.get_files("python_help")
osl.run_python_file(paths1[0])
print(osl.run_python_file(paths2[0]))

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
# .. image:: ../../../_static/04_python_node_and_help.png
#  :width: 300
#  :alt: Result of script.
#
#########################################################
