PyOptiSLang Documentation |version|
===================================

.. toctree::
   :hidden:
   :maxdepth: 3

   getting_started/index
   user_guide/index
   api/index
   examples/index
   contributing/index


Introduction
-------------
Ansys optiSLang is a constantly evolving, leading-edge answer to the challenges posed 
by CAE-based Robust Design Optimization (RDO). Its state-of-the-art algorithms efficiently 
and automatically search for the most robust design configuration, eliminating the slow, 
manual process that used to define RDO.

What is PyOptiSLang?
--------------------
PyOptiSLang is part of the larger `PyAnsys <https://docs.pyansys.com>`_
effort to facilitate the use of Ansys technologies directly from
Python. 
PyOptiSLang implements a client-server architecture. It uses TCP/IP technology to launch or connect 
with a running optiSLang process as a server. However, you only need to interact with the Python 
interface. You can use PyOptiSLang to programmatically create, interact with, and control 
an optiSLang project, create customizable scripts that will speed-up and automate simulations. 
PyOptiSLang  lets you use optiSLang within a Python environment of your choice 
in conjunction with other PyAnsys libraries and external Python libraries.

Features
--------
Package ``ansys-optislang-core`` provides:
   - Launching of optiSLang locally or remote connection to optiSLang. For more information, 
     see :ref:`ref_launch`.
   - Basic server commands and queries to get information about projects and its status. For more 
     information, see :ref:`ref_functions`.
   - Running of python scripts based on Ansys optiSLang Python API.  For more infornmation, 
     see :ref:`ref_run_python`.
  
Documentation and issues
------------------------
In addition to installation and usage information, the PyOptiSLang documentation provides 
an :ref:`ref_index_api`, :ref:`ref_examples`, and :ref:`ref_contributing` guidelines.

On the `PyOptiSLang Issues <https://github.com/pyansys/pyoptislang/issues>`_ page, you can create 
issues to submit questions, report bugs, and request new features. To reach the PyAnsys support 
team, email pyansys.support@ansys.com.


Project Index
*************

* :ref:`genindex`