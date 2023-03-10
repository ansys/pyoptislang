
===============
Troubleshooting
===============

This section explains how to resolve the most common issues encountered 
with ``ansys-optislang-core``. In order to get more details about error, increase logging level by
parameter ``loglevel`` when launching optiSLang:

.. code:: python

    from ansys.optislang.core import Optislang

    osl = Optislang(loglevel="DEBUG")
    osl.dispose()

Common issues
-------------

Timeout error when launching optiSLang
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Default timeout for launching optiSLang is 20 seconds. This can be increased by parameter ``ini_timeout``
when launching optiSLang:

.. code:: python

    from ansys.optislang.core import Optislang

    osl = Optislang(ini_timeout=30)
    osl.dispose()


