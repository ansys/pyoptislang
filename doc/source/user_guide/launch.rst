.. _ref_launch:

=====================================
Initial setup and launching optiSLang
=====================================
In order to run, ``ansys.optislang.core`` needs to know the location of the optiSLang.
Most of the time this can be automatically determined, but non-standard installs needs 
to provide the location of optiSLang. You can start optiSLang by running:

.. code:: python

    from ansys.optislang.core import Optislang
    osl = Optislang()
    print(osl)
    osl.dispose()


List of all automatically detected, supported executables of optiSLang can be obtained by running:

.. code:: python

    from ansys.optislang.core import utils
    print(utils.find_all_osl_exec())

By default, the newest version is used when launching optiSLang. In order to launch specific version
from list preceding, launch :class:`Optislang <ansys.optislang.core.optislang.Optislang>` with parameter 
``executable`` containing path to desired version:

.. code:: python

    from ansys.optislang.core import Optislang
    osl = Optislang(executable = r'C:\\Program Files\\Dynardo\\Ansys optiSLang\\2023 R1\\optislang.com')
    print(osl)
    osl.dispose()

In order to open specific project or create new one, launch 
:class:`Optislang <ansys.optislang.core.optislang.Optislang>` with parameter
``project_path``, example below shows creating new project in current working directory:

.. code:: python

    import os
    from ansys.optislang.core import Optislang
    
    path = os.getcwd()
    project_name = 'test.opf'

    osl = Optislang(project_path = os.path.join(path, project_name))
    print(osl)
    osl.dispose()

Connect to a remote instance of optiSLang
-----------------------------------------
For remote connection, it is assumed that the optiSLang server process is already running
on remote (or local) host. In that case, the host and port must be specified and parameters
related to the execution of the new optiSLang server are ignored.

.. code:: python

     from ansys.optislang.core import Optislang
     osl = Optislang(host = "127.0.0.1", port = 49690)
     print(osl)
     osl.dispose()
