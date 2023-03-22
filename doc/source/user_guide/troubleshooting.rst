
===============
Troubleshooting
===============

This page explains how to resolve the most common issues encountered 
with the ``ansys-optislang-core`` package. To get more detailed
information about an error, when launching optiSLang, use the
``loglevel`` parameter:

.. code:: python

    from ansys.optislang.core import Optislang

    osl = Optislang(loglevel="DEBUG")
    osl.dispose()


Timeout error when launching optiSLang
--------------------------------------
The default timeout for launching optiSLang is 20 seconds. When launching
optiSLang, you can use the ``ini_timeout`` parameter to increase the timeout:

.. code:: python

    from ansys.optislang.core import Optislang

    osl = Optislang(ini_timeout=30)
    osl.dispose()
