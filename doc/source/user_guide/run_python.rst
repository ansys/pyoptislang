.. _ref_run_python:

================================================
Executing commands from the optiSLang Python API
================================================
When optiSLang is active, you can send individual python commands to it as a genuine a
Python class. For example, if you want to get general information about sensitivity actor, 
you would call:

.. code:: python

    from ansys.optislang.core import Optislang

    osl = Optislang()
    print(osl.run_python_script("""help(actors.SensitivityActor)"""))
    osl.dispose()

.. note:: 
    Be aware that each time 
    :func:`run_python_script() <ansys.optislang.core.optislang.Optislang.run_python_script>` 
    is called, new python console is created inside optiSLang, so variables from previous calls 
    won't be available.

For longer scripts, instead of sending string to optiSLang as in the preceding
example, it is possible to send path to python script and it's converted to
string automatically, example below crates workflow with 2 variable actors and
calculator (see example :ref:`ref_simple_calculator`):

.. code:: python

    from ansys.optislang.core import Optislang
    from ansys.optislang.core import examples

    osl = Optislang()
    path_to_file = examples.get_files("simple_calculator")[0]
    osl.run_python_file(file_path=path_to_file)
    osl.dispose()
