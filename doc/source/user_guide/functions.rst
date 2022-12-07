.. _ref_functions:

===========
Basic usage
===========
In order to start project, use :func:`start <ansys.optislang.core.optislang.Optislang.start>`
(example :ref:`ref_simple_calculator` can be used):

.. code:: python
    
    from pathlib import Path
    from ansys.optislang.core import Optislang
    from ansys.optislang.core import examples
    osl = Optislang()
    path_to_file = examples.get_files('simple_calculator')[0]
    osl.run_python_file(file_path=path_to_file)
    osl.start()

In order to save the current project, use either
:func:`save() <ansys.optislang.core.optislang.Optislang.save>`,
:func:`save_as() <ansys.optislang.core.optislang.Optislang.save_as>` or
:func:`save_copy() <ansys.optislang.core.optislang.Optislang.save_copy>`:

.. code:: python
    project_path = Path().cwd() / "test_project.opf"
    osl.save_as(project_path)

Please note that optiSLang project is located in a temporary directory if an instance 
of :class:`Optislang() <ansys.optislang.core.optislang.Optislang>` was created with default 
settings, so either :func:`save_as() <ansys.optislang.core.optislang.Optislang.save_as>` or
:func:`save_copy() <ansys.optislang.core.optislang.Optislang.save_copy>` must be used at first.


In order to create or open existing or create new project, methods
:func:`new() <ansys.optislang.core.optislang.Optislang.save>` or
:func:`open() <ansys.optislang.core.optislang.Optislang.save_as>` may be used. 

.. code:: python
    new_project = Path().cwd() / "new_project.opf"
    osl.new()
    osl.save_as(new_project)

Some general info about project can be obtained by running:

.. code:: python

    print(osl)

Or via running specific requests:

.. code:: python

    print(f'Version: {osl.get_osl_version_string()}')
    print(f'Description: {osl.get_project_description()}')
    print(f'Location: {osl.get_project_location()}')
    print(f'Name: {osl.get_project_name()}')
    print(f'Status: {osl.get_project_status()}')

When the :class:`Optislang() <ansys.optislang.core.optislang.Optislang>` instance is no longer 
needed, terminate connection with optiSLang server by running:

.. code:: python

    osl.dispose()