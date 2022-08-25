"""
.. _ref_oscillator_robustness:

Oscillator robustness
---------------------

Create robustness flow for oscillator python example (using ``oscillator_robustness_arsm.py``)
and run this flow. Save optiSLang project into the same folder as this script then.
More details in python script and oscillator example in optiSLang tutorial section.
"""

import os

from ansys.optislang.core import Optislang
import ansys.optislang.core.examples as examples

# in current working directory, create dir for osl files
path = os.path.dirname(__file__)
osl_files_path = os.path.join(path, "optislang_projects", "02_1_oscillator_robustness")
os.makedirs(osl_files_path, exist_ok=True)

osl = Optislang()
paths = examples.get_files("oscillator_robustness_arsm")
osl.run_python_script(paths[0])
osl.save_copy(os.path.join(osl_files_path, "test_project.opf"))
osl.start()
osl.save_copy(os.path.join(osl_files_path, "test_project.opf"))
osl.shutdown()
