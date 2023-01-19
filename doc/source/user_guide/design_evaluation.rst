.. _ref_design_evaluation:

==================
Design evaluation
==================
Instance of the :class:`RootSystem() <ansys.optislang.core.nodes.RootSystem>` allows user to
create new designs and evaluate them. This feature is currently supported only 
on the project level and parameters have to be already defined in the project. Instance of the 
:class:`RootSystem() <ansys.optislang.core.nodes.RootSystem>` is accessible from instance of the 
:class:`Optislang() <ansys.optislang.core.optislang.Optislang>`.

.. code:: python
    
    from ansys.optislang.core import Optislang
    from ansys.optislang.core.project_parametric import Design
    from ansys.optislang.core import examples
    from pathlib.Path import Path

    parametric_project = examples.get_files('calculator_with_params')[1][0]
    osl = Optislang(project_path=parametric_project)
    osl.save_as(Path.cwd() / 'parametric_project.opf')
    root_system = osl.project.root_system


Get reference design
--------------------
Design with all parameters specified in the project with their reference values can be obtained by 
:func:`get_reference_design() <ansys.optislang.core.nodes.RootSystem.create_design>` method. 
Parameters values may be modified by methods of the instance of
:class:`Design() <ansys.optislang.core.project_parametric.Design>` class.

.. code:: python
    
    from ansys.optislang.core.project_parametric import DesignVariable
    reference_design = root_system.get_reference_design()
    # modify value of parameter using either ``parameter`` and ``value``
    reference_design.set_parameter_by_name(parameter = 'a', value = 12)
    # instance of DesignVariable or Parameter may be used as well
    a = DesignVariable(name='a', value=12)
    reference_design.set_parameter(parameter=a)


Create new design
-----------------
Design can be also created from scratch and there are 2 ways of doing it, either by method 
:func:`create_design() <ansys.optislang.core.nodes.RootSystem.create_design>` of the
:class:`RootSystem() <ansys.optislang.core.nodes.RootSystem>` instance or directly
creating instance of the :class:`Design() <ansys.optislang.core.project_parametric.Design>` class.
Parameters don't have to be provided when initializing new design.

.. code:: python
    
    # design created using directly Design() class
    direct_design = Design(parameters = {'a': 3, 'b': 4})
    # create empty design and add parameters afterward
    empty_design = Design()
    empty_design.set_parameter_by_name(parameter = 'a', value = 3)
    empty_design.set_parameter_by_name(parameter = 'q', value = 4)
    # parameters may also be removed
    empty_design.remove_parameter(name = 'c')
    # or remove all parameters
    empty_design.clear_parameters()


Check design structure
----------------------
In order to check whether design contains all parameters defined in project, methods
:func:`get_missing_parameters_names() <ansys.optislang.core.nodes.RootSystem.get_missing_parameters_names>` and
:func:`get_undefined_parameters_names() <ansys.optislang.core.nodes.RootSystem.get_undefined_parameters_names>` 
may be used. This step is not necessary though, because this is always done internally when 
evaluating design.

.. code:: python

    missing_parameters = root_system.get_missing_parameters(empty_design)
    undefined_parameters = root_system.get_undefined_parameters(direct_design)


Evaluate design
---------------
Designs can be evaluated using method
:func:`evaluate_design() <ansys.optislang.core.nodes.RootSystem.evaluate_design>`. This method 
returns the same instance of :class:`Design() <ansys.optislang.core.project_parametric.Design>` 
class with updated results.

.. code:: python

    # single design
    result_design = root_system.evaluate_design(design = reference_design)

.. note:: 
    
    Please note that optiSLang retains only last evaluated design at RootSystem level. Therefore,
    results of previous designs have to be stored locally if they are required for further usage,
    e.g. as an instance of :class:`Design() <ansys.optislang.core.project_parametric.Design>` class.
    
Finally, when everything is done and 
:class:`Optislang() <ansys.optislang.core.optislang.Optislang>` instance is not needed any more,
terminate it.

.. code:: python

    osl.dispose()







