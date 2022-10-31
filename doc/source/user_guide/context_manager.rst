.. _ref_context_manager:

Context manager
---------------
It is supported (and recommended) to use 
:class:`Optislang() <ansys.optislang.core.optislang.Optislang>` as a context manager. Main advantage
of this approach is that instance of :class:`Optislang() <ansys.optislang.core.optislang.Optislang>`
and connection to optiSLang server will be terminated correctly even if an error occurs 
or if user forgets to terminate it gracefully either via 
:func:`dispose() <ansys.optislang.core.optislang.Optislang.dispose>`
or :func:`shutdown() <ansys.optislang.core.optislang.Optislang.shutdown>`.

.. code:: python
    
    from ansys.optislang.core import Optislang
    from ansys.optislang.core import examples
    with Optislang() as osl:
        path_to_file = examples.get_files('simple_calculator')[0]
        osl.run_python_file(file_path=path_to_file)
        osl.start()

In case of error (or generally when ``__exit__`` method of context manager is called), commands
based on use case will be executed:

#. The optiSLang server was launched by an instance of
   :class:`Optislang() <ansys.optislang.core.optislang.Optislang>`:
    * launched with parameter `shutdown_on_finished=True`, default
        * terminate optiSLang server
    * launched with parameter `shutdown_on_finished=False`
        * terminate connection to optiSLang server, keep server running
  
#. The :class:`Optislang <ansys.optislang.core.optislang.Optislang>` instance has connected to
   a remote (or already running local) optiSLang server.

    * terminate connection to optiSLang server, keep server running
