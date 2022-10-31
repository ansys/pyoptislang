.. _ref_user_guide:

==========
User guide
==========
This guide provides a general overview of the basics and usage of the
PyOptiSLang library.

.. toctree::
   :maxdepth: 1
   :hidden:
   
   launch
   functions
   run_python
   context_manager
   troubleshooting


PyOptiSLang basic overview
--------------------------
The instance of the :class:`Optislang <ansys.optislang.core.optislang.Optislang>` class 
within the ``ansys-optislang-core`` library can be used to control and query the optiSLang project.

OptiSLang can be started from Python using
:class:`Optislang() <ansys.optislang.core.optislang.Optislang>`. This starts
optiSLang in a temporary directory by default. Path to the project file can be specified 
by the ``project_path`` parameter of the 
:func:`Optislang() <ansys.optislang.core.optislang.Optislang>` as follows:

.. code:: python

    import os
    from ansys.optislang.core import Optislang

    path = os.getcwd()
    file_name = 'test_optislang.opf'
    osl = Optislang(project_path = os.path.join(path, file_name))
    osl.dispose()


If the project file exists, it is opened; otherwise, a new project file is created on the specified 
path. Please note that :class:`Optislang <ansys.optislang.core.optislang.Optislang>` 
instance should be gracefully terminated either via 
:func:`dispose() <ansys.optislang.core.optislang.Optislang.dispose>` or
:func:`shutdown() <ansys.optislang.core.optislang.Optislang.shutdown>` when it's no longer in use.


Difference in these termination methods is that method
:func:`dispose() <ansys.optislang.core.optislang.Optislang.dispose>` only terminates connection
with optiSLang server, method
:func:`shutdown() <ansys.optislang.core.optislang.Optislang.shutdown>` additionally sends command
to terminate server, which is necessary when (server is started locally by instance of
:class:`Optislang <ansys.optislang.core.optislang.Optislang>` with parameter 
`shutdown_on_finished=False` or connected to a remote optiSLang server) AND termination of optiSLang
server is requested. 


The :class:`Optislang <ansys.optislang.core.Optislang>` class provides several functions which 
enable to control or query the project. The following example shows how to open an existing project 
and run it using the :func:`start() <ansys.optislang.core.optislang.Optislang.start>` function.

.. code:: python

    from ansys.optislang.core import Optislang
    from ansys.optislang.core import examples
    
    project_path = examples.get_files('simple_calculator')[1]
    osl = Optislang(project_path = project_path)
    osl.start()
    osl.dispose()

Currently, the capabilities provided by the ``ansys-optislang-core`` library are limited. 
However, this can be overcome using the 
:func:`run_python_script() <ansys.optislang.core.optislang.Optislang.run_python_script>` or
:func:`run_python_file() <ansys.optislang.core.optislang.Optislang.run_python_file>` functions of 
the :class:`Optislang <ansys.optislang.core.optislang.Optislang>` class. 
Both functions provide the ability to execute commands of the ``optiSLang Python API``. 
Executing commands from ``optiSLang Python API`` is currently the only possibility to create and edit 
new nodes, parameters etc. These features may be added in the future versions of the ``ansys-optislang-core`` library. 
For more information, see :ref:`ref_run_python`.
