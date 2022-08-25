"""
.. _ref_simple_calculator:

Simple calculator
-----------------

Create a simple flow of 4 nodes a run this flow then (using ``simple_calculator.py``).

     A(12.0)  ---
                  | --->  A + B*2  ---> Result
     B( 3.0)  ---

Save optiSLang project into the same folder as this script then.
More details in python script.
"""

import os

from ansys.optislang.core import Optislang
import ansys.optislang.core.examples as examples

# in current working directory, create dir for osl files
path = os.path.dirname(__file__)
osl_files_path = os.path.join(path, "optislang_projects", "07_simple_calculator")
os.makedirs(osl_files_path, exist_ok=True)

osl = Optislang()
paths = examples.get_files("simple_calculator")
osl.run_python_script(paths[0])
osl.save_copy(os.path.join(osl_files_path, "test_project.opf"))
osl.start()
osl.save_copy(os.path.join(osl_files_path, "test_project.opf"))
osl.shutdown()
