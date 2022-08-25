"""
.. _ref_oscillator_python_systems:

Oscillator python systems
-------------------------

Create parametric system for oscillator python example (using ``oscillator_system_python.py``)
and run it. Save optiSLang project into the same folder as this script then.
More details in python script and oscillator example in optiSLang tutorial section.
"""

import os

from ansys.optislang.core import Optislang
import ansys.optislang.core.examples as examples

# in current working directory, create dir for osl files
path = os.path.dirname(__file__)
osl_files_path = os.path.join(path, "optislang_projects", "02_2_python_system")
os.makedirs(osl_files_path, exist_ok=True)

osl = Optislang()
paths = examples.get_files("oscillator_system_python")
osl.run_python_script(paths[0])
osl.save_copy(os.path.join(osl_files_path, "test_project.opf"))
osl.start()
osl.save_copy(os.path.join(osl_files_path, "test_project.opf"))
osl.shutdown()
