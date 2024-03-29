.. _ref_user_guide:

==========
User guide
==========
This section provides an overview of how you use PyOptiSLang.

.. toctree::
   :maxdepth: 1
   :hidden:

   launch
   functions
   project_content
   design_evaluation
   create_workflow
   run_python
   osl_server_usage
   troubleshooting


With the :py:class:`Optislang <ansys.optislang.core.optislang.Optislang>` class
in PyOptiSLang, you can launch optiSLang as a server and then control and query
optiSLang projects.

The following code shows how to launch OptiSLang from Python. By default,
optiSLang is started in a temporary directory. Using the ``project_path``
parameter, you can specify a path to a project file. If this project file exists,
it is opened. Otherwise, a new project file is created in the specified path.
For more information, see :ref:`ref_launch`.

.. code:: python

    import os
    from ansys.optislang.core import Optislang
    from pathlib import Path

    path = Path.cwd()
    file_name = "test_optislang.opf"
    with Optislang(project_path=path / file_name) as osl:
        print(osl)


The :py:class:`Optislang <ansys.optislang.core.Optislang>` class provides several methods for
controlling or querying the project. This code shows how to open an existing project
and run it using the :py:meth:`start() <ansys.optislang.core.project.Project.start>` method.

.. code:: python

  from ansys.optislang.core import Optislang
  from ansys.optislang.core import examples

  project_path = examples.get_files("simple_calculator")[1][0]
  with Optislang(project_path=project_path) as osl:
      osl.application.project.start()


While the current capabilities provided by PyOptiSLang are limited, you can
use the :py:meth:`run_python_script() <ansys.optislang.core.project.Project.run_python_script>`
or :py:meth:`run_python_file() <ansys.optislang.core.project.Project.run_python_file>`
method in the :py:class:`Project <ansys.optislang.core.project.Project>` class
to overcome its limitations. For example, you can run optiSLang Python API commands
to create and edit nodes, parameters, and more. For more information, see :ref:`ref_run_python`.

Another possibility is to use direct communication with the optiSLang server API using the
:py:class:`TcpOslServer <ansys.optislang.core.tcp.osl_server.TcpOslServer>` wrapper class.
For more information, see :ref:`ref_osl_server_usage`.
