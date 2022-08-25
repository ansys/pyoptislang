"""
.. _ref_python_node_and_help:

Python node and help
--------------------

Create a Python2 node and add some source code, add and remove parameters and responses, add
internal variables (using ``python_node.py``). Print which nodes are available in python
console (using ``python_help.py``). Save optiSLang project into the same folder as this script
then. More details in python script.
"""

import os

from ansys.optislang.core import Optislang
import ansys.optislang.core.examples as examples

# in current working directory, create dir for osl files
path = os.path.dirname(__file__)
osl_files_path = os.path.join(path, "optislang_projects", "04_python_node_and_help")
os.makedirs(osl_files_path, exist_ok=True)

osl = Optislang()
paths1 = examples.get_files("python_node")
paths2 = examples.get_files("python_help")
osl.run_python_script(paths1[0])
print(osl.run_python_script(paths2[0]))
osl.save_copy(os.path.join(osl_files_path, "test_project.opf"))
osl.shutdown()
