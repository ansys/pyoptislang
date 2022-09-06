"""
.. _ref_oscillator_oscillator_calibration_systems:

Oscillator calibration systems
------------------------------

Create parametric systems for oscillator calibration python example (using
``oscillatorcalibration_system_python.py`` and ``oscillatorcalibration_system_ascii.py``)
and run these system. Save optiSLang project into the same folder as this script then.
More details in individual python scripts and oscillator example in optiSLang tutorial section.
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
paths1 = examples.get_files("oscillatorcalibration_system_python")
paths2 = examples.get_files("oscillatorcalibration_system_ascii")

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
# .. image:: ../../_static/02_5_oscillator_calibration_systems.png
#  :width: 400
#  :alt: Result of script.
#
#########################################################
