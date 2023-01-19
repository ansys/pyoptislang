"""
.. _ref_optimizer_settings:

Optimizer settings
------------------

Create, configure and insert an Evolutionary Algorithm Optimizer into the scenery
(using ``optimizer_settings.py``). Save optiSLang project into the same folder as this script
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
# in current working directory, create dir for osl files
osl = Optislang()
print(osl)

#########################################################
# Get path of example script and run it.
#########################################################
paths = examples.get_files("optimizer_settings")
osl.run_python_file(paths[0])

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
# .. image:: ../../../_static/05_optimizer_settings.png
#  :width: 300
#  :alt: Result of script.
#
#########################################################
