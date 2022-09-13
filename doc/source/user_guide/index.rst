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
The instance of the :class:`Optislang <ansys.optislang.core.Optislang>` class 
within the ``ansys-optislang-core`` library can be used to control and query the optiSLang project.

OptiSLang can be started from Python using
:func:`Optislang() <ansys.optislang.core.Optislang>`. This starts
optiSLang in a temporary directory by default. Path to the project file can be specified 
by the ``project_path`` parameter of the :func:`Optislang() <ansys.optislang.core.Optislang>` as follows:

.. code:: python

    import os
    from ansys.optislang.core import Optislang

    path = os.getcwd()
    file_name = 'test_optislang.opf'
    osl = Optislang(project_path = os.path.join(path, file_name))
    osl.shutdown()


If the project file exists, it is opened; otherwise, a new project file is created on the specified path. 
Please note that the :func:`shutdown() <ansys.optislang.core.Optislang.shutdown>` function should be executed 
when the :class:`Optislang <ansys.optislang.core.Optislang>` instance is no more needed.

The :class:`Optislang <ansys.optislang.core.Optislang>` class provides several functions which enable to control or query the project. 
The following example shows how to open an existing project and run it using the :func:`start() <ansys.optislang.core.Optislang.start>` function.

.. code:: python

    from ansys.optislang.core import Optislang
    from ansys.optislang.core import examples
    
    project_path = examples.get_files('simple_calculator')[1]
    osl = Optislang(project_path = project_path)
    osl.start()
    osl.shutdown()

Currently, the functionality provided by the ``ansys-optislang-core`` library is limited. 
However, this can be overcome using the :func:`run_python_script() <ansys.optislang.core.Optislang.run_python_script>` or
:func:`run_python_file() <ansys.optislang.core.Optislang.run_python_file>` functions of 
the :class:`Optislang <ansys.optislang.core.Optislang>` class. 
Both functions provide the ability to execute commands of the ``optiSLang Python API``. 
Executing commands from ``optiSLang Python API`` is currently the only possibility to create and edit 
new nodes, parameters etc. These features will be added in the future versions of the ``ansys-optislang-core`` library. 
For more information, see :ref:`ref_run_python`.