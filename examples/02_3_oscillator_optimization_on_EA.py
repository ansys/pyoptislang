"""
.. _ref_oscillator_optimization_on_EA:

Oscillator optimization on EA
-----------------------------

Create direct optimization using evolutionary algorithm flow for oscillator python example
(using ``oscillator_optimization_ea.py``) and run this flow. Save optiSLang project into
the same folder as this script then. More details in python script and oscillator example
in optiSLang tutorial section.
"""

import os

from ansys.optislang.core import Optislang
import ansys.optislang.core.examples as examples

# in current working directory, create dir for osl files
path = os.path.dirname(__file__)
osl_files_path = os.path.join(path, "optislang_projects", "02_3_optimization_on_EA")
os.makedirs(osl_files_path, exist_ok=True)


osl = Optislang()
paths = examples.get_files("oscillator_optimization_ea")
osl.run_python_script(paths[0])
osl.save_copy(os.path.join(osl_files_path, "test_project.opf"))
osl.start()
osl.save_copy(os.path.join(osl_files_path, "test_project.opf"))
osl.shutdown()
