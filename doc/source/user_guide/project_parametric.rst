.. _ref_project_parametric:

==================
Project parametric
==================
Instance of the :class:`Optislang() <ansys.optislang.core.optislang.Optislang>` allows user to
create new designs and evaluate them. This feature is currently supported only on the project
level and parameters have to be defined beforehand.

Parameters
----------
There are 2 ways of getting list of project parameters. Either via built-in method 
:func:`get_parameters_list() <ansys.optislang.core.optislang.Optislang.get_parameters_list>` of the
:class:`Optislang() <ansys.optislang.core.optislang.Optislang>` instance or using instance of the
:class:`ParameterManager() <ansys.optislang.core.optislang.project_parametric.ParameterManager>`.
Second way allows user to get detailed info about individual parameters and functionality
of adding new parameters shall be implemented in the future.

.. code:: python
    
    from ansys.optislang.core import Optislang
    from ansys.optislang.core.project_parametric import Design
    from ansys.optislang.core import examples
    from pathlib.Path import Path

    parametric_project = examples.get_files('calculator_with_params')[1]
    osl = Optislang(project_path=parametric_project)
    osl.save_copy(Path.cwd() / 'parametric_project.opf')
    
    # Using Optislang() method.
    parameters_list = osl.get_parameters_list()
    # Using ParameterManager.
    parameter_manager = osl.get_parameter_manager()
    parameters_list = parameter_manager.parameters_list
    parameters_dict = parameter_manager.parameters 

Create new design
-----------------
There are 2 ways of creating new design. Either via built in method 
:func:`create_design() <ansys.optislang.core.optislang.Optislang.create_design>` of the
:class:`Optislang() <ansys.optislang.core.optislang.Optislang>` instance or directly
creating instance of :class:`Design() <ansys.optislang.core.project_parametric.Design>`.
Parameters must not be provided when creating new design.

.. code:: python
    
    # design created using Optislang() method
    design_by_osl = osl.create_design(parameters = {'a': 1, 'b': 2})
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

    osl.validate_design(direct_design)

Evaluate design
---------------
Designs might be evaluated individually using method
:func:`evaluate_design() <ansys.optislang.core.optislang.Optislang.evaluate_design>`
or multiple designs might be evaluated using method
:func:`evaluate_multiple_designs() <ansys.optislang.core.optislang.Optislang.evaluate_multiple_designs>`.

.. code:: python

    # single design
    parameters, responses = osl.evaluate_design(design = design_by_osl)
    print(f'Input parameters: {parameters}')
    print(f'Responses: {responses}')
    
    # multiple designs
    outputs = osl.evaluate_multiple_designs(designs = [direct_design, design])
    for output in outputs:
        print(f'Input parameters: {output[0]}')
        print(f'Responses: {output[1]}')
    
Finally, when everything is done and 
:class:`Optislang() <ansys.optislang.core.optislang.Optislang>` instance is not needed any more,
terminate it.

.. code:: python

    osl.dispose()







