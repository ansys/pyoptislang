"""
.. _ref_oscillator_optimization_on_EA:

Oscillator optimization on EA
-----------------------------

Create direct optimization using evolutionary algorithm flow for oscillator python example
(using ``oscillator_optimization_ea.py``) and run this flow. Save optiSLang project into
the same folder as this script then. More details in python script and oscillator example
in optiSLang tutorial section.
"""

####################################################
# Import necessary modules.
####################################################
from ansys.optislang.core import Optislang
import ansys.optislang.core.examples as examples

#########################################################
# Create ``Optislang()`` instance.
#########################################################
osl = Optislang()
print(osl)

#########################################################
# Get paths of example scripts and run them.
#########################################################
paths = examples.get_files("oscillator_optimization_ea")
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
# .. image:: ../../_static/02_3_optimization_on_EA.png
#  :width: 400
#  :alt: Result of script.
#
#########################################################
