.. _ref_user_guide:

==========
User guide
==========
This section provides an overview of PyOptiSLang and how you use it.

.. toctree::
   :maxdepth: 1
   :hidden:
   
   launch
   functions
   project_content
   design_evaluation
   run_python
   troubleshooting


You use the :class:`Optislang <ansys.optislang.core.optislang.Optislang>` class 
within PyOptiSLang to launch optiSLang as a server and then control and query
optiSLang projects.

The following code shows how to launch OptiSLang from Python. By default,
optiSLang is started in a temporary directory. Using the ``project_path``
parameter, you can specify a path to a project file. If this project file exists,
it is opened. Otherwise, a new project file is created in the specified path. 

.. code:: python

    import os
    from ansys.optislang.core import Optislang
    from pathlib import Path

    path = Path.cwd()
    file_name = "test_optislang.opf"
    with Optislang(project_path=path / file_name) as osl:
        print(osl)


For more information, see :ref:`ref_launch`.

The :class:`Optislang <ansys.optislang.core.Optislang>` class provides several methods for
controlling or querying the project. This code shows how to open an existing project 
and run it using the :func:`start() <ansys.optislang.core.optislang.Optislang.start>` method.

.. code:: python

    from ansys.optislang.core import Optislang
    from ansys.optislang.core import examples

    project_path = examples.get_files("simple_calculator")[1][0]
    with Optislang(project_path=project_path) as osl:
        osl.start()

  
While the current capabilities provided by PyOptiSLang are limited, you can
overcome use the :func:`run_python_script() <ansys.optislang.core.optislang.Optislang.run_python_script>`
or :func:`run_python_file() <ansys.optislang.core.optislang.Optislang.run_python_file>`
method in the :class:`Optislang <ansys.optislang.core.optislang.Optislang>` class. For
example, you can run optiSLang Python API commands to create and edit nodes, parameters,
and more. For more information, see :ref:`ref_run_python`.
