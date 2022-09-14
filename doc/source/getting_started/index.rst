Getting Started
===============
In order to run PyOptiSLang, user must have access to licensed copy of optiSLang. The first 
supported supported version of optiSLang is 2023R1. For more information about optiSLang, visit the 
`optiSLang <https://www.ansys.com/products/connect/ansys-optislang>`_ page on the Ansys website.

************
Installation
************

Python Module
~~~~~~~~~~~~~
The ``ansys-optislang-core`` package currently supports python 3.7 through 3.10 on Windows and Linux.
Install the latest release from `PyPi
<https://pypi.org/project/ansys-optislang-core/>`_ with:

.. code::

   pip install ansys-optislang-core

Alternatively, install the latest from `PyOptiSLang GitHub
<https://github.com/pyansys/pyoptislang/releases>`_ via:

.. code::

   pip install git+https://github.com/pyansys/pyoptislang.git


For a local "development" version, install with:

.. code::

   git clone https://github.com/pyansys/pyoptislang.git
   cd pyoptislang
   pip install -e .

This will allow you to install the PyOptiSLang ``ansys-optislang-core`` module
and modify it locally and have the changes reflected in your setup
after restarting the Python kernel.

Offline installation
~~~~~~~~~~~~~~~~~~~~
If the machine, where the installation is to be performed doesn't have internet connection, the 
recommended way of installing PyOptiSLang is downloading archive from `Releases Page 
<https://github.com/pyansys/pyoptislang/releases>`_ for your corresponding setup.

For example, on Linux with Python 3.7, unzip it and install it with the following:

.. code:: bash

    unzip PyOptiSLang-v0.01.dev1-wheelhouse-Linux-3.7.zip wheelhouse
    pip install ansys-optislang-core -f wheelhouse --no-index --upgrade --ignore-installed

If you're on Windows with Python 3.9, unzip to a wheelhouse directory and install using the same 
command as above.

Consider installing using a `virtual environment
<https://docs.python.org/3/library/venv.html>`_.


Ansys Software Requirements
~~~~~~~~~~~~~~~~~~~~~~~~~~~
Ansys optiSLang version >= 2023R1.


Verify installation
~~~~~~~~~~~~~~~~~~~

.. code:: python

    >>> from ansys.optislang.core import Optislang
    >>> osl = Optislang()
    >>> print(osl)
    >>> osl.shutdown()

If you see a response from the server, congratulations!  You're ready
to get started using OptiSLang as a service.  For details regarding the
PyOptiSLang interface, see :ref:`ref_user_guide`.