.. _ref_launch:

=============================
Optislang instance management
=============================
The instance of the :class:`Optislang <ansys.optislang.core.optislang.Optislang>` class 
within the ``ansys-optislang-core`` library can be used to control and query the optiSLang project.
Instance of
:class:`Optislang <ansys.optislang.core.optislang.Optislang>` can either launch optiSLang server
locally or it may connect to already running optiSLang server. Please note that 
:class:`Optislang <ansys.optislang.core.optislang.Optislang>`  instance should be always terminated 
gracefully when it's no longer in use by calling
:func:`dispose() <ansys.optislang.core.optislang.Optislang.dispose>` method. Therefore, it is 
recommended to use instance of :class:`Optislang <ansys.optislang.core.optislang.Optislang>` 
as a context manager, that will execute 
:func:`dispose() <ansys.optislang.core.optislang.Optislang.dispose>` method automatically even
when exception is raised.


Launching optiSLang locally
---------------------------
In order to run, :class:`Optislang <ansys.optislang.core.optislang.Optislang>` needs to know 
the location of the optiSLang executable. By default, the latest installed version is used when 
launching optiSLang. To initialize :class:`Optislang <ansys.optislang.core.optislang.Optislang>` 
instance and start optiSLang server locally, run the following script:

.. code:: python

    from ansys.optislang.core import Optislang
    osl = Optislang()
    print(osl)
    osl.dispose()

Calling of :func:`dispose() <ansys.optislang.core.optislang.Optislang.dispose>` method 
closes connection with optiSLang server. If 
:class:`Optislang <ansys.optislang.core.optislang.Optislang>` instance was started with parameter
``shutdown_on_finished=True`` (default), server will shutdown automatically. If the server is
supposed to remain running after disposing 
:class:`Optislang <ansys.optislang.core.optislang.Optislang>` instance, please see chapter 
:ref:`optislang-termination`.

List of all automatically detected, supported executables of optiSLang can be obtained by running:

.. code:: python

    from ansys.optislang.core import utils
    print(utils.find_all_osl_exec())

In order to launch specific version either from the preceding list or from non-standart install 
location, launch :class:`Optislang <ansys.optislang.core.optislang.Optislang>` with parameter 
``executable`` containing path to desired executable:

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


Connect to a remote optiSLang server
------------------------------------
For remote connection, it is assumed that the optiSLang server process is already running
on remote (or local) host. In that case, the host and port must be specified and parameters
related to the execution of the new optiSLang server are ignored. To initialize 
:class:`Optislang <ansys.optislang.core.optislang.Optislang>` instance and connect to the remote 
optiSLang server, run the following script:

.. code:: python

     from ansys.optislang.core import Optislang
     
     host = "127.0.0.1"     # please specify host
     port = 5310            # please specify port

     osl = Optislang(host = host, port = port)
     print(osl)
     osl.dispose()

Calling of :func:`dispose() <ansys.optislang.core.optislang.Optislang.dispose>` method 
closes connection with remote optiSLang server. If optiSLang server was started with parameter
``shutdown_on_finished=False``, server won't shutdown. If shutdown of the optiSLang server
is requested :func:`shutdown() <ansys.optislang.core.optislang.Optislang.shutdown>` has to be called
before disposing, please see following chapter.

.. _optislang-termination:

Optislang instance disposal and optional optiSLang server shutdown
------------------------------------------------------------------
Please note that :class:`Optislang <ansys.optislang.core.optislang.Optislang>` 
instance should be always gracefully terminated when it's no longer in use by 
:func:`dispose() <ansys.optislang.core.optislang.Optislang.dispose>` method. OptiSLang server may be
optionally terminated by :func:`shutdown() <ansys.optislang.core.optislang.Optislang.shutdown>` 
(this must be done before :func:`dispose() <ansys.optislang.core.optislang.Optislang.dispose>`
method and it's not needed when started with default parameter ``shutdown_on_finished=True``).


Difference in the termination methods mentioned above is that:

* :func:`dispose() <ansys.optislang.core.optislang.Optislang.dispose>` only closes connection
  with optiSLang server,

* :func:`shutdown() <ansys.optislang.core.optislang.Optislang.shutdown>` sends command
  to shutdown server, which is necessary when termination of optiSLang server is requested 
  and either:

    * server is started locally by instance of
      :class:`Optislang <ansys.optislang.core.optislang.Optislang>` with parameter 
      ``shutdown_on_finished=False``, OR

    * :class:`Optislang <ansys.optislang.core.optislang.Optislang>` is connected to a remote 
      optiSLang server. 


To specify whether to automatically shutdown the optiSLang server, the ``shutdown_on_finished``
can be used in :class:`Optislang <ansys.optislang.core.optislang.Optislang>` instance constructor. 
Default value is ``shutdown_on_finished=True``. This means that optiSLang server is shutdown 
automatically after :func:`dispose() <ansys.optislang.core.optislang.Optislang.dispose>` method 
is called. In order to keep locally started optiSLang server running even after disposing
:class:`Optislang <ansys.optislang.core.optislang.Optislang>` instance, parameter 
``shutdown_on_finished=False`` must be used when creating new instance. In such case,
:func:`shutdown() <ansys.optislang.core.optislang.Optislang.shutdown>` may be called before
disposing instance of :class:`Optislang <ansys.optislang.core.optislang.Optislang>` in order
to shutdown optiSLang server.

The following examples show possible termination cases of 
:class:`Optislang <ansys.optislang.core.optislang.Optislang>` instance initialized 
with parameter ``shutdown_on_finished=False``:

#. In order to keep optiSLang server running, use only 
   :func:`dispose() <ansys.optislang.core.optislang.Optislang.dispose>` method:
 
    * .. code:: python

        from ansys.optislang.core import Optislang
    
        osl = Optislang(shutdown_on_finished=False)
        print(osl)
        osl.dispose()

#. In order to shutdown optiSLang server, use both 
   :func:`shutdown() <ansys.optislang.core.optislang.Optislang.shutdown>` and
   :func:`dispose() <ansys.optislang.core.optislang.Optislang.dispose>` method:

    * .. code:: python

        from ansys.optislang.core import Optislang
    
        osl = Optislang(shutdown_on_finished=False)
        print(osl)
        osl.shutdown()
        osl.dispose()

The same approach can be used when connected to a remote optiSLang server.

+-----------------+----------------------------+----------------+----------------------------------+
| Initialization  | ``shutdown_on_finished``   | **Commands**   | **optiSLang server is running**  |
+=================+============================+================+==================================+
| **Local**       | ``True``                   | ``dispose()``  | **NO**                           |
|                 +----------------------------+----------------+----------------------------------+
|                 | ``False``                  | ``dispose()``  | **YES**                          |
|                 |                            +----------------+----------------------------------+
|                 |                            | ``shutdown()`` | **NO**                           |
|                 |                            | ``dispose()``  |                                  |
+-----------------+----------------------------+----------------+----------------------------------+
| **Remote**      | ``True``                   | ``dispose()``  | **NO**                           |
|                 +----------------------------+----------------+----------------------------------+
|                 | ``False``                  | ``dispose()``  | **YES**                          |
|                 |                            +----------------+----------------------------------+
|                 |                            | ``shutdown()`` | **NO**                           |
|                 |                            | ``dispose()``  |                                  |
+-----------------+----------------------------+----------------+----------------------------------+


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
