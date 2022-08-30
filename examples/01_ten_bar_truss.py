"""
.. _ref_ten_bar_truss:

Ten bar truss
-------------

Create ARSM ten_bar_truss flow in batch (using ``arsm_ten_bar_truss.py``),
modify this flow (using ``ten_bar_modify_parameters`` and ``ten_bar_truss_lc2``),
run this project (and optionally save_copy). More details in individual python scripts and
ten bar truss example in optiSLang tutorial section.
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
paths1 = examples.get_files("arsm_ten_bar_truss")
paths2 = examples.get_files("ten_bar_modify_parameters")
paths3 = examples.get_files("ten_bar_truss_lc2")

osl.run_python_script(paths1[0])
osl.run_python_script(paths2[0])
osl.run_python_script(paths3[0])

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
