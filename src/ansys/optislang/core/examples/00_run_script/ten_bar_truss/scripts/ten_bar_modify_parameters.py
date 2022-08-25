"""Modify parameters."""
###############################################################################
# (c) 2021 ANSYS, Inc. Unauthorized use, distribution, or duplication is prohibited.
#
# modify flow created by arsm_ten_bar_truss.py
# set lowerbounds of a parameter
# run following command from command line:
# optislang ten_bar_arsm.opf --batch --python ten_bar_modify_parameters.py --no-run

# or choose this file after selecting "Run script file" from Python console's
# context menu
###############################################################################
from py_os_design import *

# import needed modules
from py_os_parameter import *

### ARSM node ###
# get the ARSM node
arsm = find_actor("ARSM")

### Parameter modification ###
# get the parameter manager of ARSM node
params = arsm.parameter_manager
# e.g. SetLowerBound to 5.0 of a parameter
params.set_bounds("area01", PyOSDesignEntry(5.0), PyOSDesignEntry(15.0))
# set parameter manager at ARSM node
arsm.parameter_manager = params
