.. _ref_context_manager:

Context manager
---------------
It is supported (and recommended) to use 
:class:`Optislang() <ansys.optislang.core.optislang.Optislang>` as a context manager. Main advantage
of this approach is that optiSLang server will be terminated correctly even if an error occurs 
or if user forgets to use :func:`dispose() <ansys.optislang.core.optislang.Optislang.dispose>`
method when :class:`Optislang <ansys.optislang.core.optislang.Optislang>` instance is no longer
in use.

.. code:: python
    
    from ansys.optislang.core import Optislang
    from ansys.optislang.core import examples
    with Optislang() as osl:
        path_to_file = examples.get_files('simple_calculator')[0]
        osl.run_python_file(file_path=path_to_file)
        osl.start()
        osl.dispose()


In case of error or omitted termination of 
:class:`Optislang() <ansys.optislang.core.optislang.Optislang>`, ``__exit__`` method of context
manager will execute commands depending on how 
:class:`Optislang() <ansys.optislang.core.optislang.Optislang>`
was launched:

#. The optiSLang server was launched by an instance of
   :class:`Optislang() <ansys.optislang.core.optislang.Optislang>`:

    * terminate optiSLang server 
  
#. The :class:`Optislang <ansys.optislang.core.optislang.Optislang>` instance has connected to
   a remote (or already running local) optiSLang server.

    * just terminate processes of :class:`Optislang <ansys.optislang.core.optislang.Optislang>` 
      instance and keep optiSLang server running
