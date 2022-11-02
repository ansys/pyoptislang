.. _ref_launch:

=====================================
Initial setup and launching optiSLang
=====================================
Instance of
:class:`Optislang <ansys.optislang.core.optislang.Optislang>` can either launch optiSLang server
locally or it may connect to already running optiSLang server. This instance should be terminated 
gracefully when it's no longer in use by calling
:func:`dispose() <ansys.optislang.core.optislang.Optislang.dispose>` method. Therefore, it is 
recommended to use instance of :class:`Optislang <ansys.optislang.core.optislang.Optislang>` 
as a context manager, that will execute 
:func:`dispose() <ansys.optislang.core.optislang.Optislang.dispose>` method automatically even
when error is raised.

Launching optiSLang locally
---------------------------
In order to run, ``ansys.optislang.core`` needs to know the location of the optiSLang.
Most of the time this can be automatically determined, but non-standard installs needs 
to provide the location of optiSLang. You can start optiSLang by running:

.. code:: python

    from ansys.optislang.core import Optislang
    osl = Optislang()
    print(osl)
    osl.dispose()


List of all automatically detected, supported executables of optiSLang can be obtained by running:

.. code:: python

    from ansys.optislang.core import utils
    print(utils.find_all_osl_exec())

By default, the newest version is used when launching optiSLang. In order to launch specific version
from list preceding, launch :class:`Optislang <ansys.optislang.core.optislang.Optislang>` with parameter 
``executable`` containing path to desired version:

.. code:: python

    from ansys.optislang.core import Optislang
    osl = Optislang(executable = r'C:\\Program Files\\Dynardo\\Ansys optiSLang\\2023 R1\\optislang.com')
    print(osl)
    osl.dispose()

In order to open specific project or create new one, launch 
:class:`Optislang <ansys.optislang.core.optislang.Optislang>` with parameter
``project_path``, example below shows creating new project in current working directory:

.. code:: python

    import os
    from ansys.optislang.core import Optislang
    
    path = os.getcwd()
    project_name = 'test.opf'

    osl = Optislang(project_path = os.path.join(path, project_name))
    print(osl)
    osl.dispose()

Keep optiSLang server running
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Default setting of optiSLang server is ``shutdown_on_finished=True``. This means that optiSLang
server is terminated automatically after 
:func:`dispose() <ansys.optislang.core.optislang.Optislang.dispose>` method was called. 
If user wishes to keep optiSLang server running even after disposing
:class:`Optislang <ansys.optislang.core.optislang.Optislang>` instance, parameter 
``shutdown_on_finished=False`` must be used when creating new instance.

.. code:: python

    from ansys.optislang.core import Optislang
    
    osl = Optislang(shutdown_on_finished=False)
    print(osl)
    osl.dispose()

In order to terminate optiSLang server launched this way, use
:func:`shutdown() <ansys.optislang.core.optislang.Optislang.shutdown>` method:

.. code:: python

    from ansys.optislang.core import Optislang
    
    osl = Optislang(shutdown_on_finished=False)
    print(osl)
    osl.shutdown()
    osl.dispose()

Connect to a remote instance of optiSLang
-----------------------------------------
For remote connection, it is assumed that the optiSLang server process is already running
on remote (or local) host. In that case, the host and port must be specified and parameters
related to the execution of the new optiSLang server are ignored.

.. code:: python

     from ansys.optislang.core import Optislang, OslServerProcess
     import time
     
     server_process = OslServerProcess(shutdown_on_finished=False, logger=logger)
     server_process.start()
     time.sleep(5)  # wait for launching of server process
     
     # connect to optiSLang server and terminate connection afterward
     osl = Optislang(host = "127.0.0.1", port = 5310)
     print(osl)
     osl.dispose()

     # connect to optiSLang server and terminate server afterward
     osl = Optislang(host = "127.0.0.1", port = 5310)
     print(osl)
     osl.shutdown()
     osl.dispose()

Context manager
---------------
It is recommended to use 
:class:`Optislang() <ansys.optislang.core.optislang.Optislang>` as a context manager. Main advantage
of this approach is that instance of :class:`Optislang() <ansys.optislang.core.optislang.Optislang>`
and connection to optiSLang server will be terminated gracefully even if an error occurs by calling
:func:`dispose() <ansys.optislang.core.optislang.Optislang.dispose>` method automatically.

.. code:: python
    
    from ansys.optislang.core import Optislang
    with Optislang() as osl:
        print(osl)
        osl.start()

.. note::

    When instance of :class:`Optislang <ansys.optislang.core.optislang.Optislang>` is started
    with argument ``shutdown_on_finished=False`` or connected to optiSLang server started with
    such setting, default behaviour is to terminate connection and keep optiSLang server running.
    In order to terminate optiSLang server, method 
    :func:`shutdown() <ansys.optislang.core.optislang.Optislang.shutdown>` has to be used.

    .. code:: python
    
        from ansys.optislang.core import Optislang
        with Optislang(shutdown_on_finished=False) as osl:
            print(osl)
            osl.start()
            osl.shutdown()
