.. _ref_user_guide:

==========
User Guide
==========
This guide provides a general overview of the basics and usage of the
PyOptiSLang library.

.. toctree::
   :maxdepth: 1
   :hidden:
   
   launch
   functions
   run_python
   troubleshooting


PyOptiSLang Basic Overview
--------------------------

The :class:`Optislang() <ansys.optislang.core.Optislang>` class
within the ``ansys-optislang-core`` library creates an instance of
:class:`Optislang <ansys.optislang.core.optislang.Optislang>` in the background and sends
commands to that service.  Errors and warnings are processed
Pythonically letting the user develop a script real-time without
worrying about if it will function correctly when deployed in batch
mode.

OptiSLang can be started from python using
:func:`Optislang() <ansys.optislang.core.Optislang>`. This starts
optiSLang in a temporary directory by default.  You can change project directory to
your current working directory and file name with:

.. code:: python

    import os
    from ansys.optislang.core import Optislang

    path = os.getcwd()
    file_name = 'test_optislang.opf'
    osl = Optislang(project_path = os.path.join(path, file_name))
    osl.shutdown()

If we wanted to open existing project and run it, we would start optiSLang with 
parameter ``project_path`` referencing to path of existing project and use function :func:`start`.

.. code:: python

    from ansys.optislang.core import Optislang
    from ansys.optislang.core import examples
    
    project_path = examples.get_files('simple_calculator')[1]
    osl = Optislang(project_path = project_path)
    osl.start()
    osl.shutdown()

When optiSLang is active, you can send individual python commands to it as a genuine a Python class 
via :func:`run_python_commands <ansys.optislang.core.optislang.Optislang.run_python_commands>`.
Executing commands from optiSLang Python API is currently the only option how to create and edit 
new nodes, parameters etc. These functionalities will be added in future versions. For more 
information, see :ref:`ref_run_python`.