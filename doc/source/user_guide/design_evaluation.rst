.. _ref_design_evaluation:

==================
Design evaluation
==================
Instance of the :class:`RootSystem() <ansys.optislang.core.nodes.RootSystem>` allows user to
create new designs and evaluate them. Instance of the 
:class:`RootSystem() <ansys.optislang.core.nodes.RootSystem>` is accessible from instance of the 
:class:`Optislang() <ansys.optislang.core.optislang.Optislang>` via its 
:func:`project <ansys.optislang.core.project.Project>` property.

.. code:: python
    
    from ansys.optislang.core import Optislang
    from ansys.optislang.core.project_parametric import Design
    from ansys.optislang.core import examples
    from pathlib.Path import Path

    # open project with defined parameters
    parametric_project = examples.get_files('calculator_with_params')[1][0]
    osl = Optislang(project_path=parametric_project)

    # do not modify original file
    osl.save_as(Path.cwd() / 'parametric_project.opf')

    # get root system
    root_system = osl.project.root_system

.. note::

    Creation and evaluation of designs is currently supported only on the 
    :class:`RootSystem() <ansys.optislang.core.nodes.RootSystem>`. Therefore, project has to have 
    parameters already defined at the project root system and workflow has to be 
    prepared for this (``Receive designs`` and ``Send back designs`` must be set in design flow).
    Please, see example :ref:`ref_ten_bar_truss_evaluate_design`.


Create new design
-----------------
New :class:`Design() <ansys.optislang.core.project_parametric.Design>` can be created by obtaining 
design with reference values from :class:`RootSystem() <ansys.optislang.core.nodes.RootSystem>` 
and modifying its parameters or design parameters can be specified from scratch.


From reference design
~~~~~~~~~~~~~~~~~~~~~
Design with all parameters specified in the project with their reference values can be obtained by 
:func:`get_reference_design() <ansys.optislang.core.nodes.RootSystem.create_design>` method. 
Parameters values may be modified by methods of the instance of
:class:`Design() <ansys.optislang.core.project_parametric.Design>` class.

.. code:: python
    
    # ...
    
    from ansys.optislang.core.project_parametric import DesignVariable

    reference_design = root_system.get_reference_design()

    # modify parameter value using either ``name`` and ``value``
    reference_design.set_parameter_by_name(name = 'a', value = 12)

    # instance of ``DesignVariable`` or ``Parameter`` may be used as well
    a = DesignVariable(name='a', value=12)
    reference_design.set_parameter(parameter=a)


From empty design
~~~~~~~~~~~~~~~~~~~
Design can be also created from scratch directly creating instance of the 
:class:`Design() <ansys.optislang.core.project_parametric.Design>` class.
Parameters don't have to be provided when initializing new design.

.. code:: python
    
    # design created using directly Design() class
    direct_design = Design(parameters = {'a': 3, 'b': 4})

    # create empty design and add parameters afterward
    empty_design = Design()
    empty_design.set_parameter_by_name(name = 'a', value = 3)
    empty_design.set_parameter_by_name(name = 'q', value = 4)

    # parameters may also be removed
    empty_design.remove_parameter(name = 'c')

    # or remove all parameters
    empty_design.clear_parameters()


Check design parameters
~~~~~~~~~~~~~~~~~~~~~~~
In order to check whether design contains all parameters defined in the project, 
:func:`get_missing_parameters_names() <ansys.optislang.core.nodes.RootSystem.get_missing_parameters_names>` 
method can be used. To check, whether design contains parameters which are not defined in the project, method
:func:`get_undefined_parameters_names() <ansys.optislang.core.nodes.RootSystem.get_undefined_parameters_names>` 
may be used. This step is not necessary though, because this is always done internally while evaluating design.

.. code:: python

    # ...

    missing_parameters = root_system.get_missing_parameters(empty_design)
    undefined_parameters = root_system.get_undefined_parameters(direct_design)


Evaluate design
---------------
Designs can be evaluated using method
:func:`evaluate_design() <ansys.optislang.core.nodes.RootSystem.evaluate_design>`. This method 
returns the same instance of :class:`Design() <ansys.optislang.core.project_parametric.Design>` 
class with updated results.

.. code:: python

    # ...

    # single design
    result_design = root_system.evaluate_design(design = reference_design)

.. note:: 
    
    Please, note that the optiSLang retains only last evaluated design at the project root system. 
    Therefore, results of previous designs have to be stored locally if they are required for 
    further usage, for example as an instance of 
    :class:`Design() <ansys.optislang.core.project_parametric.Design>` class.
    
Finally, when everything is done and 
:class:`Optislang() <ansys.optislang.core.optislang.Optislang>` instance is not needed any more,
terminate it.

.. code:: python

    osl.dispose()







