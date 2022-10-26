"""
.. _ref_python_node_and_help:

Python node and help
--------------------

Create a Python2 node and add some source code, add and remove parameters and responses, add
internal variables (using ``python_node.py``). Print which nodes are available in python
console (using ``python_help.py``). Save optiSLang project into the same folder as this script
then. More details in python script.
"""

####################################################
# Import necessary modules.
####################################################
from ansys.optislang.core import Optislang
import ansys.optislang.core.examples as examples

#################################################################################
# Create :class:`Optislang <ansys.optislang.core.optislang.Optislang>` instance.
#################################################################################
osl = Optislang()
print(osl)

#########################################################
# Get paths of example scripts and run them.
#########################################################
paths1 = examples.get_files("python_node")
paths2 = examples.get_files("python_help")
osl.run_python_file(paths1[0])
print(osl.run_python_file(paths2[0]))

######################################################################
# In order to save project to desired location, uncomment lines below:
# .. code:: python
#
#   path = r'<insert-desired-location>'
#   osl.save_copy(os.path.join(path, "test_project.opf"))
#
######################################################################

#########################################################
# Terminate and cancel project.
#########################################################
osl.shutdown()

#########################################################
# Generated workflow:
# .. image:: ../../_static/04_python_node_and_help.png
#  :width: 300
#  :alt: Result of script.
#
#########################################################
