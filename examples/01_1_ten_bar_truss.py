"""
.. _ref_ten_bar_truss:

Ten bar truss
-------------

Create ARSM ten_bar_truss flow in batch (using ``arsm_ten_bar_truss.py``),
modify this flow (using ``ten_bar_modify_parameters`` and ``ten_bar_truss_lc2``),
run this project and save_copy. More details in individual python scripts and
ten bar truss example in optiSLang tutorial section.
"""

import os

from ansys.optislang.core import Optislang
import ansys.optislang.core.examples as examples

# in current working directory, create dir for osl files
# path = os.path.dirname(inspect.getfile(inspect.currentframe()))
path = os.path.dirname(__file__)
osl_files_path = os.path.join(path, "optislang_projects", "01_1_ten_bar_truss")
os.makedirs(osl_files_path, exist_ok=True)

osl = Optislang()
paths1 = examples.get_files("arsm_ten_bar_truss")
paths2 = examples.get_files("ten_bar_modify_parameters")
paths3 = examples.get_files("ten_bar_truss_lc2")

osl.run_python_script(paths1[0])
osl.run_python_script(paths2[0])
osl.run_python_script(paths3[0])
osl.save_copy(os.path.join(osl_files_path, "test_project.opf"))
osl.start()
osl.save_copy(os.path.join(osl_files_path, "test_project.opf"))
osl.shutdown()
