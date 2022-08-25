"""Create workflow."""
##############################################################################
# (c) 2021 ANSYS, Inc. Unauthorized use, distribution, or duplication is prohibited.

# TODO Add internal variables from oscillator example project

# Set up a parametric system containing text input, Abaqus process actor and
# Abaqus ETK output actor. Based on the oscillator example.
##############################################################################

import os

from py_os_design import *
from py_osl3binfile import *
from stdcpp_python_export import Path

# get example path "OSL_EXAMPLES": .\pyoptislang\src\ansys\optislang\core\examples
my_odb = os.path.join(
    os.environ["OSL_EXAMPLES"], "00_run_script", "etk_abaqus", "files", "oscillator.odb"
)
my_inp = os.path.join(
    os.environ["OSL_EXAMPLES"], "00_run_script", "etk_abaqus", "files", "oscillator.inp"
)

##############################################################################
# Create parametric system
pss = actors.ParametricSystemActor()
add_actor(pss)

##############################################################################
# Add text input actor

input_actor = actors.TextInputActor("inp_file")
input_actor.file_path = Path(my_inp)
input_actor.set_content()

# Define input parameters
input_actor.add_parameter(actors.TextInputActor.Parameter("m", 26, 8, 3))
input_actor.add_parameter(actors.TextInputActor.Parameter("k", 27, 8, 3))
input_actor.add_parameter(actors.TextInputActor.Parameter("D", 28, 8, 4))
input_actor.add_parameter(actors.TextInputActor.Parameter("Ekin", 29, 8, 3))

pss.add_actor(input_actor)
connect(pss, "IODesign", input_actor, "IDesign")

##############################################################################
# Add Abaqus process actor
process_actor = actors.AbaqusProcessActor("abq_process")
process_actor.abaqus_base = Path("abaqus")
process_actor.job_name = "oscillator_expl"

pss.add_actor(process_actor)
connect(input_actor, "ODesign", process_actor, "IDesign")

##############################################################################
# Add ETK Abaqus output actor

odb = actors.ETKAbaqusActor("abaqus_01")
odb.path = Path(my_odb)

# Variable: disp

etk_var = odb.ODBHistoryOutputVariable(Path(my_odb), "disp")
etk_var.region_name = "Node MASS-1.1"
etk_var.step_name = "Explicit"
etk_var.history_output_name = "U1"
odb.register_as_internal_location(etk_var)

# Variable: disp_peaks
odb.add_expression(actors.DerivedLocation("disp_peaks", "peaks(disp)"))

# Variable: disp_max

# Variable: omega_damped

pss.add_actor(odb)

connect(process_actor, "ODesign", odb, "IDesign")
connect(odb, "ODesign", pss, "IIDesign")
