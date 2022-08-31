.. _ref_user_guide:

==========
User Guide
==========
This guide provides a general overview of the basics and usage of the
PyOptiSLang library.


PyOptiSLang Basic Overview
==========================

The :func:`Optislang() <ansys.optislang.core.Optislang>` function
within the ``ansys-optislang-core`` library creates an instance of of
:class:`Optislang <ansys.optislang.core.optislang.Optislang>` in the background and sends
commands to that service.  Errors and warnings are processed
Pythonically letting the user develop a script real-time without
worrying about if it will function correctly when deployed in batch
mode.

OptiSLang can be started from python using
:func:`Optislang() <ansys.optislang.core.Optislang>`. This starts
optiSLang in a temporary directory by default.  You can change this to
your current directory with:

.. code:: python

    import os
    from ansys.optislang.core import Optislang

    path = os.getcwd()
    osl = Optislang(run_location=path)

optiSLang is now active and you can send individual python commands to it as a genuine a
Python class.  For example, if we wanted to create sensitivity node and change it's number of
sampling points and sampling method, we would run:

.. code:: python

    from ansys.optislang.core import Optislang
    
    osl = Optislang()
    osl.run_python_commands(
    """
    import py_doe_settings
    from dynardo_py_algorithms import DOETYPES
    sensitivity = actors.SensitivityActor('My_Sensitivity_Actor_Commands')
    add_actor(sensitivity)
    sensitivity_system = find_actor('My_Sensitivity_Actor_Commands')
    new_settings = sensitivity_system.algorithm_settings
    new_settings.num_discretization = 200
    new_settings.sampling_method = DOETYPES.PLAINMONTECARLO
    sensitivity_system.algorithm_settings = new_settings
    """
    )

.. note:: 
    Be aware that each time ``run_python_commands`` is called, new python console is created 
    inside optiSLang, so variable from previous calls won't be available.

For longer scripts, instead of sending string to optiSLang as in the above example, we can instead 
send path to script and it's converted to string automatically:

.. code:: python

    from ansys.optislang.core import Optislang
    from ansys.optislang.core import examples
    path_to_script = examples.get_files('sensitivity_settings')[0]
    osl.run_python_script(script_path=path_to_script)