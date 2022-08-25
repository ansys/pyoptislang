"""
.. _ref_oscillator_oscillator_MOP_sensitivity_and_optimization:

Oscillator sensitivity and optimization on MOP
----------------------------------------------

Create sensitivity flow for oscillator python example (using ``oscillator_sensitivity_mop.py``)
and optimization on mop flow (using ``oscillator_optimization_on_mop.py``) and run these flows.
Save optiSLang project into the same folder as this script then. More details in individual
python scripts and oscillator example in optiSLang tutorial section.
"""

import os

from ansys.optislang.core import Optislang
import ansys.optislang.core.examples as examples

# in current working directory, create dir for osl files
path = os.path.dirname(__file__)
osl_files_path = os.path.join(
    path, "optislang_projects", "02_4_oscillator_MOP_sensitivity_and_optimization"
)
os.makedirs(osl_files_path, exist_ok=True)

osl = Optislang()
paths1 = examples.get_files("oscillator_sensitivity_mop")
paths2 = examples.get_files("oscillator_optimization_on_mop")

osl.run_python_script(paths1[0])
osl.run_python_script(paths2[0])
osl.save_copy(os.path.join(osl_files_path, "test_project.opf"))
osl.start()
osl.save_copy(os.path.join(osl_files_path, "test_project.opf"))
osl.shutdown()
