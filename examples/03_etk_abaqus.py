"""
.. _ref_etk_abaqus:

ETK Abaqus
----------

Set up a parametric system containing text input, Abaqus process actor and Abaqus ETK output
actor (using ``etk_abaqus.py``). Save optiSLang project into the same folder as this script
then. More details in python script and oscillator example in optiSLang tutorial section.
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
paths = examples.get_files("etk_abaqus")
osl.run_python_file(paths[0])

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
# .. image:: ../../_static/03_etk_abaqus.png
#  :width: 400
#  :alt: Result of script.
#
#########################################################
