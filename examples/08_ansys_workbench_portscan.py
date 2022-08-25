"""
.. _ref_portscan:

Ansys workbench portscan
------------------------

Check for free ports in a specific range (default=49690-49700)
(using ``ansys_workbench_portscan.py``), print output then. More details in python script.
"""

from ansys.optislang.core import Optislang
import ansys.optislang.core.examples as examples

osl = Optislang()
paths = examples.get_files("ansys_workbench_portscan")
print(osl.run_python_script(paths[0]))
osl.shutdown()
