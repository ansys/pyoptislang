.. _ref_functions:

===========
Basic usage
===========
In order to start project, use :func:`start <ansys.optislang.core.optislang.Optislang.start>`
(example :ref:`ref_simple_calculator` can be used):

.. code:: python
    
    import os
    from ansys.optislang.core import Optislang
    from ansys.optislang.core import examples
    osl = Optislang()
    path_to_file = examples.get_files('simple_calculator')[0]
    osl.run_python_file(file_path=path_to_file)
    osl.start()

In order to save current project, use 
:func:`save_copy() <ansys.optislang.core.optislang.Optislang.save_copy>`:

.. code:: python

    osl.save_copy(os.path.join(os.getcwd(), "test_project.opf"))

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