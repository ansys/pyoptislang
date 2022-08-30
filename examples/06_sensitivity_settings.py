"""
.. _ref_sensitivity_settings:

Sensitivity settings
--------------------

At first create a system named "Sensitivity". Then find system "Sensitivity and change some
of its settings (using ``sensitivity_settings.py``). Save optiSLang project into the same
folder as this script then. More details in python script.
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
# Get path of example script and run it.
#########################################################
paths = examples.get_files("sensitivity_settings")
osl.run_python_script(paths[0])

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