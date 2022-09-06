Getting Started
===============
Local licensed copy or remote instance of optiSLang needs to be installed. The first supported 
supported version is 2023R1. For more information about OptiSLang, visit the 
`OptiSLang <https://www.ansys.com/products/connect/ansys-optislang>`_ page on the Ansys website.

************
Installation
************

Python Module
~~~~~~~~~~~~~
The ``ansys-optislang-core`` package currently supports python 3.7 through 3.10 on Windows and Linux.
Two installation modes are provided: user and developer.

For users
~~~~~~~~~

In order to install PyOptiSLang core, make sure you
have the required build system tool. To do so, run:

.. code:: bash

    python -m pip install -U pip flit

Then, you can simply execute command below to install latest release:

.. code:: bash

    python -m pip install ansys-optislang-core

Alternatively, install the latest release from PyOptiSLang GitHub by executing:

.. code:: bash

    python -m pip install git+https://github.com/pyansys/pyoptislang.git

Local "development" version
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Installing PyoptiSLang core in developer mode allows you to modify the source and enhance it. 
More detailed information about installation in :ref:`ref_contributing`.

.. code:: bash

    git clone https://github.com/pyansys/pyoptislang.git
    cd pyoptislang
    pip install -e .

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