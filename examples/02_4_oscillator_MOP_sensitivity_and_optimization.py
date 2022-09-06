"""
.. _ref_oscillator_oscillator_MOP_sensitivity_and_optimization:

Oscillator sensitivity and optimization on MOP
----------------------------------------------

Create sensitivity flow for oscillator python example (using ``oscillator_sensitivity_mop.py``)
and optimization on mop flow (using ``oscillator_optimization_on_mop.py``) and run these flows.
Save optiSLang project into the same folder as this script then. More details in individual
python scripts and oscillator example in optiSLang tutorial section.
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
paths1 = examples.get_files("oscillator_sensitivity_mop")
paths2 = examples.get_files("oscillator_optimization_on_mop")

osl.run_python_file(paths1[0])
osl.run_python_file(paths2[0])


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
# .. image:: ../../_static/02_4_oscillator_MOP_sensitivity_and_optimization.png
#  :width: 600
#  :alt: Result of script.
#
#########################################################
