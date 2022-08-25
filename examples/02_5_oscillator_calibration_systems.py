"""
.. _ref_oscillator_oscillator_calibration_systems:

Oscillator calibration systems
------------------------------

Create parametric systems for oscillator calibration python example (using
``oscillatorcalibration_system_python.py`` and ``oscillatorcalibration_system_ascii.py``)
and run these system. Save optiSLang project into the same folder as this script then.
More details in individual python scripts and oscillator example in optiSLang tutorial section.
"""

import os

from ansys.optislang.core import Optislang
import ansys.optislang.core.examples as examples

# in current working directory, create dir for osl files
path = os.path.dirname(__file__)
osl_files_path = os.path.join(path, "optislang_projects", "02_5_oscillator_calibration_systems")
os.makedirs(osl_files_path, exist_ok=True)

osl = Optislang()
paths1 = examples.get_files("oscillatorcalibration_system_python")
paths2 = examples.get_files("oscillatorcalibration_system_ascii")

osl.run_python_script(paths1[0])
osl.run_python_script(paths2[0])
osl.save_copy(os.path.join(osl_files_path, "test_project.opf"))
osl.start()
osl.save_copy(os.path.join(osl_files_path, "test_project.opf"))
osl.shutdown()
