PyOptiSLang
===========
|pyansys| |python| |pypi| |GH-CI| |codecov| |MIT| |black|

.. |pyansys| image:: https://img.shields.io/badge/Py-Ansys-ffc107.svg?logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAIAAACQkWg2AAABDklEQVQ4jWNgoDfg5mD8vE7q/3bpVyskbW0sMRUwofHD7Dh5OBkZGBgW7/3W2tZpa2tLQEOyOzeEsfumlK2tbVpaGj4N6jIs1lpsDAwMJ278sveMY2BgCA0NFRISwqkhyQ1q/Nyd3zg4OBgYGNjZ2ePi4rB5loGBhZnhxTLJ/9ulv26Q4uVk1NXV/f///////69du4Zdg78lx//t0v+3S88rFISInD59GqIH2esIJ8G9O2/XVwhjzpw5EAam1xkkBJn/bJX+v1365hxxuCAfH9+3b9/+////48cPuNehNsS7cDEzMTAwMMzb+Q2u4dOnT2vWrMHu9ZtzxP9vl/69RVpCkBlZ3N7enoDXBwEAAA+YYitOilMVAAAAAElFTkSuQmCC
   :target: https://docs.pyansys.com/
   :alt: PyAnsys

.. |python| image:: https://img.shields.io/badge/Python-%3E%3D3.7-blue
   :target: https://pypi.org/project/pyoptislang/
   :alt: Python

.. |pypi| image:: https://img.shields.io/pypi/v/pyoptislang.svg?logo=python&logoColor=white
   :target: https://pypi.org/project/pyoptislang
   :alt: PyPI

.. |codecov| image:: https://codecov.io/gh/pyansys/pyoptislang/branch/main/graph/badge.svg
   :target: https://codecov.io/gh/pyansys/pyoptislang
   :alt: Codecov

.. |GH-CI| image:: https://github.com/pyansys/pyoptislang/actions/workflows/ci_cd.yml/badge.svg
   :target: https://github.com/pyansys/pyoptislang/actions/workflows/ci_cd.yml
   :alt: GH-CI

.. |MIT| image:: https://img.shields.io/badge/License-MIT-yellow.svg
   :target: https://opensource.org/licenses/MIT
   :alt: MIT

.. |black| image:: https://img.shields.io/badge/code%20style-black-000000.svg?style=flat
   :target: https://github.com/psf/black
   :alt: Black


Overview
--------
The PyOptiSLang project is a python wrapper for Ansys optiSLang applicattion. It supports Pythonic 
access to OptiSLang to be able to communicate with OptiSLang process directly from python. 
The latest ansys-optislang-core package supports:

- Remote connections to OptiSLang via TCP/IP.
- Basic server commands, queries and running of python scripts.

Documentation and issues
------------------------
See the latest release of the `Documentation <https://optislangdocs.pyansys.com>`_ for more detailed 
information on PyOptiSLang. Issues, bug reports, request for new features or other questions can 
be addressed to `PyOptiSLang Issues <https://github.com/pyansys/pyoptislang/issues>`_.

Installation
------------
The ``ansys-optislang-core`` package currently supports python 3.7 through 3.10 on Windows and Linux.
Install the latest release from `PyPi
<https://pypi.org/project/ansys-optislang-core/>`_ with:

.. code::

   pip install ansys-optislang-core

Alternatively, install the latest from `PyOptiSLang GitHub
<https://github.com/pyansys/pyoptislang/issues>`_ via:

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

    unzip PyOptiSLang-v0.1.0-wheelhouse-Linux-3.7.zip wheelhouse
    pip install ansys-optislang-core -f wheelhouse --no-index --upgrade --ignore-installed

If you're on Windows with Python 3.9, unzip to a wheelhouse directory and install using the same 
command as above.

Dependencies
--------------
Local licensed copy or remote instance of Optislang needs to be installed. The first supported 
version is 2023R1.

Getting started
---------------

Launch optiSLang locally 
~~~~~~~~~~~~~~~~~~~~~~~~

You can launch optiSLang locally using ``Optislang()``, both ``host`` and ``port`` parameters 
must be ``None``, other parameters can be optionally specified.:

.. code:: python
    
    from ansys.optislang.core import Optislang
    osl = Optislang()
    osl.shutdown()

Connect to a remote optiSLang server
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For remote connection, it is assumed that the OptiSLang server process is already running
on remote (or local) host. In that case, the host and port must be specified and parameters
related to the execution of the new optiSLang server are ignored.:

.. code:: python
    
    from ansys.optislang.core import Optislang
    host = "127.0.0.1"
    port = 5310
    osl = Optislang(host=host, port=port)
    osl.shutdown()

Basic usage
~~~~~~~~~~~

.. code:: python

    from ansys.optislang.core import Optislang
    osl = Optislang()
    file_path = r"C:\Users\Username\my_scripts\myscript.py"
    osl.run_python_file(path=script_path)
    osl.save_copy("MyNewProject.opf")
    osl.shutdown()

License and acknowledgments
---------------------------

PyOptiSLang is licensed under the MIT license.

This module, ``ansys-optislang-core`` makes no commercial claim over Ansys whatsoever. This module 
extends the functionality of ``OptiSLang`` by adding a Python interface to OptiSLang without 
changing the core behavior or license of the original software. The use of the interactive control 
of ``PyOptiSLang`` requires a legally licensed local copy of OptiSLang. For more information about 
OptiSLang, visit the `OptiSLang <https://www.ansys.com/products/connect/ansys-optislang>`_ page 
on the Ansys website.