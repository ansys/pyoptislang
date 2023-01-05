.. _ref_design_evaluation:

==================
Design evaluation
==================
Instance of the :class:`RootSystem() <ansys.optislang.core.nodes.RootSystem>` allows user to
create new designs and evaluate them. This feature is currently supported only 
on the project level and parameters have to be defined beforehand. Instance of the 
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
    
    reference_design = root_system.get_reference_design()
    # modify value of first parameter
    reference_design.set_parameter(parameter = 'a', value = 12)


Create new design
-----------------
Design can be also created from scratch and there are 2 ways of doing it, either by method 
:func:`create_design() <ansys.optislang.core.nodes.RootSystem.create_design>` of the
:class:`RootSystem() <ansys.optislang.core.nodes.RootSystem>` instance or directly
creating instance of the :class:`Design() <ansys.optislang.core.project_parametric.Design>` class.
Parameters don't have to be provided when initializing new design.

.. code:: python
    
    # design created using RootSystem() method
    design_by_osl = root_system.create_design(parameters = {'a': 1, 'b': 2})
    # design created using directly Design() class
    direct_design = Design(parameters = {'a': 3, 'b': 4})
    # create empty design and add parameters afterward
    design = Design()
    design.set_parameter(parameter = 'a', value = 5)
    design.set_parameters(parameters = {'b': 6, 'c': 7, 'd': 8, 'f': 9})
    # parameters may also be removed
    design.remove_parameters(to_be_removed = 'c')
    design.remove_parameters(to_be_removed = ['d', 'f'])


Validate design
---------------
In order to check whether design contains all parameters defined in project, method
:func:`validate_design() <ansys.optislang.core.optislang.Optislang.validate_design>` may be used.
This step is not necessary though, because this is always done internally when evaluating design.

.. code:: python

    root_system.validate_design(direct_design)


Evaluate design
---------------
Designs might be evaluated individually using method
:func:`evaluate_design() <ansys.optislang.core.nodes.RootSystem.evaluate_design>`
or multiple designs might be evaluated using method
:func:`evaluate_multiple_designs() <ansys.optislang.core.nodes.RootSystem.evaluate_multiple_designs>`.
Both of these functions return parameters and responses for convenience, but these are stored in
the used instance of :class:`Design() <ansys.optislang.core.project_parametric.Design>` as well and
may be accessed later.

.. code:: python

    # single design
    parameters, responses = root_system.evaluate_design(design = design_by_osl)
    print(f'Input parameters: {parameters}')
    print(f'Responses: {responses}')
    
    # multiple designs
    outputs = osl.evaluate_multiple_designs(designs = [direct_design, design])
    for index, output in enumerate(outputs):
        print(f'---{index}---')
        print(f'Input parameters: {output[0]}')
        print(f'Responses: {output[1]}')
    
Finally, when everything is done and 
:class:`Optislang() <ansys.optislang.core.optislang.Optislang>` instance is not needed any more,
terminate it.

.. code:: python

    osl.dispose()







