.. _ref_functions:

===========
Basic usage
===========
To start a project, you use the :func:`start <ansys.optislang.core.optislang.Optislang.start>`
method. This code starts the project for the :ref:`ref_simple_calculator` example:

.. code:: python

    from pathlib import Path
    from ansys.optislang.core import Optislang, examples

    osl = Optislang()
    path_to_file = examples.get_files("simple_calculator")[0]
    osl.run_python_file(file_path=path_to_file)
    osl.start()


To save the project, use the
:func:`save() <ansys.optislang.core.optislang.Optislang.save>`,
:func:`save_as() <ansys.optislang.core.optislang.Optislang.save_as>`, or
:func:`save_copy() <ansys.optislang.core.optislang.Optislang.save_copy>`
method. This code uses the :func:`save_as() <ansys.optislang.core.optislang.Optislang.save_as>`
method:

.. code:: python

    project_path = Path().cwd() / "test_project.opf"
    osl.save_as(project_path)


If an optiSLang instance is created with the default parameters, the optiSLang project
is located in a temporary directory. Therefore, if you want to preserve the project
permanently, you should use either the
:func:`save_as() <ansys.optislang.core.optislang.Optislang.save_as>` or
:func:`save_copy() <ansys.optislang.core.optislang.Optislang.save_copy>` method.

In order to create a new project or open an existing one, methods
:func:`new() <ansys.optislang.core.optislang.Optislang.new>` or
:func:`open() <ansys.optislang.core.optislang.Optislang.open>` may be used. 

.. code:: python

    new_project = Path().cwd() / "new_project.opf"
    osl.new()
    osl.save_as(new_project)

Some general info about project can be obtained by running:

.. code:: python

    print(osl)

Or via running specific requests:

.. code:: python

    print(f"Version: {osl.get_osl_version_string()}")
    print(f"Working directory: {osl.get_working_dir()}")

When the :class:`Optislang() <ansys.optislang.core.optislang.Optislang>` instance is no longer 
needed, close the connection with optiSLang server by running:

.. code:: python

    osl.dispose()
