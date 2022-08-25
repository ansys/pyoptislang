"""
.. _ref_ten_bar_truss2:

Ten bar truss
-------------

Create a project with workbench node (using ``ansys_workbench_ten_bar_truss.py``)
and save_copy. More details in python script.
"""

import os

from ansys.optislang.core import Optislang
import ansys.optislang.core.examples as examples

# in current working directory, create dir for osl files
path = os.path.dirname(__file__)
osl_files_path = os.path.join(path, "optislang_projects", "01_2_ten_bar_truss")
os.makedirs(osl_files_path, exist_ok=True)

# compatible with version 212
executable = r"C:\Program Files\ANSYS Inc\v212\optiSLang\optislang.exe"
osl = Optislang(executable=executable)
paths = examples.get_files("ansys_workbench_ten_bar_truss")
osl.run_python_script(paths[0])
osl.save_copy(os.path.join(osl_files_path, "test_project.opf"))
# osl.start()
# osl.save_copy(os.path.join(osl_files_path, 'test_project.opf'))
osl.shutdown()
