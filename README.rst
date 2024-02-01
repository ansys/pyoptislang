PyOptiSLang
===========
|pyansys| |python| |pypi| |PyPIact| |GH-CI| |codecov| |MIT| |black|

.. |pyansys| image:: https://img.shields.io/badge/Py-Ansys-ffc107.svg?logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAIAAACQkWg2AAABDklEQVQ4jWNgoDfg5mD8vE7q/3bpVyskbW0sMRUwofHD7Dh5OBkZGBgW7/3W2tZpa2tLQEOyOzeEsfumlK2tbVpaGj4N6jIs1lpsDAwMJ278sveMY2BgCA0NFRISwqkhyQ1q/Nyd3zg4OBgYGNjZ2ePi4rB5loGBhZnhxTLJ/9ulv26Q4uVk1NXV/f///////69du4Zdg78lx//t0v+3S88rFISInD59GqIH2esIJ8G9O2/XVwhjzpw5EAam1xkkBJn/bJX+v1365hxxuCAfH9+3b9/+////48cPuNehNsS7cDEzMTAwMMzb+Q2u4dOnT2vWrMHu9ZtzxP9vl/69RVpCkBlZ3N7enoDXBwEAAA+YYitOilMVAAAAAElFTkSuQmCC
   :target: https://docs.pyansys.com/
   :alt: PyAnsys

.. |python| image:: https://img.shields.io/badge/Python-%3E%3D3.7-blue
   :target: https://pypi.org/project/pyoptislang/
   :alt: Python

.. |pypi| image:: https://img.shields.io/pypi/v/ansys-optislang-core.svg?logo=python&logoColor=white
   :target: https://pypi.org/project/ansys-optislang-core/

.. |PyPIact| image:: https://img.shields.io/pypi/dm/ansys-optislang-core.svg?label=PyPI%20downloads
   :target: https://pypi.org/project/ansys-optislang-core/

.. |codecov| image:: https://codecov.io/gh/ansys/pyoptislang/branch/main/graph/badge.svg
   :target: https://codecov.io/gh/ansys/pyoptislang
   :alt: Codecov

.. |GH-CI| image:: https://github.com/ansys/pyoptislang/actions/workflows/ci_cd.yml/badge.svg
   :target: https://github.com/ansys/pyoptislang/actions/workflows/ci_cd.yml
   :alt: GH-CI

.. |MIT| image:: https://img.shields.io/badge/License-MIT-yellow.svg
   :target: https://opensource.org/licenses/MIT
   :alt: MIT

.. |black| image:: https://img.shields.io/badge/code%20style-black-000000.svg?style=flat
   :target: https://github.com/psf/black
   :alt: Black


Overview
--------
PyOptiSLang is a Python wrapper for Ansys optiSLang. It supports Pythonic
access to Ansys optiSLang to be able to communicate with Ansys optiSLang directly from Python.
The latest ``ansys-optislang`` package provides these capabilities:

- Starting and managing local instances of Ansys optiSLang
- Remote connections to Ansys optiSLang instances via TCP/IP
- Create new Ansys optiSLang project
- Open existing Ansys optiSLang project
- Control Ansys optiSLang project execution
- Save Ansys optiSLang project
- Execute classic Ansys optiSLang Python API script on backend side
- Evaluate designs on root project level


Documentation and issues
------------------------
For comprehensive information on PyOptiSLang, see the latest release
`documentation <https://optislang.docs.pyansys.com>`_. On the
`PyOptiSLang Issues <https://github.com/ansys/pyoptislang/issues>`_ page,
you can create issues to submit questions, report bugs, and request new features.
This is the best place to post questions and code.

Installation
------------
The ``ansys-optislang-core`` package supports Python 3.7 through 3.11 on
Windows and Linux. Three modes of installation are available:

- User installation
- Developer installation
- Offline installation

For either a developer or offline installation, consider using a `virtual environment
<https://docs.python.org/3/library/venv.html>`_.

User installation
~~~~~~~~~~~~~~~~~
Install the latest release from `PyPi
<https://pypi.org/project/ansys-optislang-core/>`_ with this command:

.. code::

   pip install ansys-optislang-core


Alternatively, install the latest `PyOptiSLang GitHub
<https://github.com/ansys/pyoptislang/issues>`_ package with this command:

.. code::

   pip install git+https://github.com/ansys/pyoptislang.git


Developer installation
~~~~~~~~~~~~~~~~~~~~~~
If you plan on doing local *development* with GitHub, clone and
install PyOptiSLang with this code:

.. code::

   git clone https://github.com/ansys/pyoptislang.git
   cd pyoptislang
   pip install -e .


A developer installation allows you to edit ``ansys-optislang-core``
files locally. Any changes that you make are reflected in your setup
after restarting the Python kernel.

Offline installation
~~~~~~~~~~~~~~~~~~~~
Using a wheelhouse can be helpful if you work for a company that restricts access to
external networks. From the `Releases <https://github.com/ansys/pyoptislang/releases>`_
page in the PyOptiSLang repository, you can find the wheelhouses for a particular release in its
assets and download the wheelhouse corresponding to your setup.

You can then install PyOptiSLang and all of its dependencies from one single entry point
that can be shared internally, which eases the security review of the PyOptiSLang package content.

For example, on Linux with Python 3.7, unzip the wheelhouse and install PyOptiSLang with code
like this:

.. code:: bash

    unzip PyOptiSLang-v0.1.0-wheelhouse-Linux-3.7.zip wheelhouse
    pip install ansys-optislang-core -f wheelhouse --no-index --upgrade --ignore-installed

If you're on Windows with Python 3.9, unzip the wheelhouse to a wheelhouse directory and
then install using the same ``pip`` command as in the preceding Linux code example.

Dependencies
--------------
You must have a local licensed copy or a remote instance of optiSLang installed. The first
supported version is 2023 R1.

Getting started
---------------
Using the ``Optislang`` class, you can either launch optiSLang locally or connect to a
remote optiSLang instance.

Launch optiSLang locally
~~~~~~~~~~~~~~~~~~~~~~~~

For launching optiSLang locally, both the ``host`` and ``port`` parameters in the ``Optislang``
class must be set to ``None``, which are their defaults. Other parameters can optionally
be specified.

.. code:: python

    from ansys.optislang.core import Optislang

    osl = Optislang()
    osl.dispose()


Connect to a remote optiSLang instance
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For remote connection, it is assumed that an optiSLang instance is already running on
a remote (or local) host as a server. In this case, you must specify the ``host`` and ``port``
parameters. Parameters related to the execution of a new optiSLang instance are ignored.

.. code:: python

    from ansys.optislang.core import Optislang

    host = "127.0.0.1"
    port = 5310
    osl = Optislang(host=host, port=port)
    osl.dispose()


Basic usage
~~~~~~~~~~~
This code shows how to launch optiSLang locally, open and run a Python
script file, save the results to a new project, and then close the
connection:

.. code:: python

    from ansys.optislang.core import Optislang

    osl = Optislang()
    file_path = r"C:\Users\Username\my_scripts\myscript.py"
    osl.application.project.run_python_file(path=file_path)
    osl.application.save_copy("MyNewProject.opf")
    osl.dispose()


License and acknowledgments
---------------------------

PyOptiSLang is licensed under the MIT license.

PyOptiSLang makes no commercial claim over Ansys whatsoever. This library extends the
functionality of Ansys optiSLang by adding a Python interface to optiSLang without
changing the core behavior or license of the original software. The use of the interactive control
of PyOptiSLang requires a legally licensed local copy of optiSLang.

For more information on optiSLang, see the `Ansys optiSLang <https://www.ansys.com/products/connect/ansys-optislang>`_
page on the Ansys website.
