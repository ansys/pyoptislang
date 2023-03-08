"""
.. _ref_oscillator_python_systems:

Oscillator python systems
-------------------------

Create parametric system for oscillator python example (using ``oscillator_system_python.py``)
and run it. Save optiSLang project into the same folder as this script then.
More details in python script and oscillator example in optiSLang tutorial section.
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
# Get path of example script and run it.
#########################################################
paths = examples.get_files("oscillator_system_python")
osl.run_python_file(paths[0])

#########################################################
# Execute workflow created by script above.
#########################################################
osl.start()

######################################################################
# In order to save project to desired location, uncomment lines below:
# .. code:: python
#
#   path = r'<insert-desired-location>'
#   osl.save_as(os.path.join(path, "test_project.opf"))
#
######################################################################

#########################################################
# Terminate and cancel project.
#########################################################
osl.dispose()

#########################################################
# Generated workflow:
# .. image:: ../../../_static/02_2_python_system.png
#  :width: 300
#  :alt: Result of script.
#
#########################################################