"""
.. _ref_etk_abaqus:

ETK Abaqus
----------

Set up a parametric system containing text input, Abaqus process actor and Abaqus ETK output
actor (using ``etk_abaqus.py``). Save optiSLang project into the same folder as this script
then. More details in python script and oscillator example in optiSLang tutorial section.
"""

import os

from ansys.optislang.core import Optislang
import ansys.optislang.core.examples as examples

# in current working directory, create dir for osl files
path = os.path.dirname(__file__)
osl_files_path = os.path.join(path, "optislang_projects", "03_etk_abaqus")
os.makedirs(osl_files_path, exist_ok=True)

osl = Optislang()
paths = examples.get_files("etk_abaqus")
osl.run_python_script(paths[0])
osl.save_copy(os.path.join(osl_files_path, "test_project.opf"))
osl.shutdown()
