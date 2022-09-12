"""
.. _ref_simple_calculator:

Simple calculator
-----------------

Create a simple flow of 4 nodes a run this flow then (using ``simple_calculator.py``).

Save optiSLang project into the same folder as this script then.
More details in python script.
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
paths = examples.get_files("simple_calculator")

#########################################################
# Get path of example script and run it.
#########################################################
osl.run_python_file(paths[0])

#########################################################
# Execute workflow created by scripts above.
#########################################################
osl.start()

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
# .. image:: ../../_static/07_simple_calculator.png
#  :width: 400
#  :alt: Result of script.
#
#########################################################
