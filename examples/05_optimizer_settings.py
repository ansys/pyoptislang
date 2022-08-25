"""
.. _ref_optimizer_settings:

Optimizer settings
------------------

Create, configure and insert an Evolutionary Algorithm Optimizer into the scenery
(using ``optimizer_settings.py``). Save optiSLang project into the same folder as this script
then. More details in python script.
"""

import os

from ansys.optislang.core import Optislang
import ansys.optislang.core.examples as examples

# in current working directory, create dir for osl files
path = os.path.dirname(__file__)
osl_files_path = os.path.join(path, "optislang_projects", "05_optimizer settings")
os.makedirs(osl_files_path, exist_ok=True)

osl = Optislang()
paths = examples.get_files("optimizer_settings")
osl.run_python_script(paths[0])
osl.save_copy(os.path.join(osl_files_path, "test_project.opf"))
osl.shutdown()
