.. _ref_project_content:

Project
-------
Instance of the :class:`Project() <ansys.optislang.core.project.Project>`, that is accessible
from the instance of :class:`Optislang() <ansys.optislang.core.optislang.Optislang>`, contains 
methods for obtaining information about loaded project and it's content.

.. code:: python
    
    from ansys.optislang.core import Optislang
    from ansys.optislang.core import examples
    from pathlib.Path import Path

    example = examples.get_files("calculator_with_params")[1][0]
    osl = Optislang(project_path=example)
    osl.save_copy(Path.cwd() / 'project_content.opf')
    project = osl.project
    
    # print project info
    print(project)
    # obtain these information directly
    name = project.get_name()
    location = project.get_location()
    status = project.get_status()


Root system and created nodes
-----------------------------
Nodes defined in the loaded project may be obtained by instance of the 
:class:`RootSystem() <ansys.optislang.core.nodes.RootSystem>`, that represents root system of
the project. Using method 
:func:`get_nodes() <ansys.optislang.core.nodes.get_nodes>` returns all nodes at the root level as
a tuple of instances of the :class:`Node() <ansys.optislang.core.nodes.Node>`,
:class:`System() <ansys.optislang.core.nodes.System>` or 
:class:`ParametricSystem() <ansys.optislang.core.nodes.ParametricSystem>`. 

.. code:: python
    
    root_system = project.root_system
    nodes = root_system.get_nodes()
    for node in nodes:
        # obtain information about node
        name = node.get_name()
        type = node.get_type()
        status = node.get_status()

If any of the obtained nodes is :class:`System() <ansys.optislang.core.nodes.System>` or 
:class:`ParametricSystem() <ansys.optislang.core.nodes.ParametricSystem>`, method 
:func:`get_nodes() <ansys.optislang.core.nodes.get_nodes>` may be used again. This is the way of 
obtaining nodes from nested systems.

Parameters
----------
In order to obtain defined parameters, instance of the 
:class:`ParameterManager() <ansys.optislang.core.project_parametric.ParameterManager>`
may be used. This class contains methods 
:func:`get_parameters() <ansys.optislang.core.project_parametric.ParameterManager.get_parameters>`, 
that returns tuple of instances of the 
:class:`OptimizationParameter() <ansys.optislang.core.project_parametric.OptimizationParameter>`,
:class:`StochasticParameter() <ansys.optislang.core.project_parametric.StochasticParameter>`,
:class:`MixedParameter() <ansys.optislang.core.project_parametric.MixedParameter>` or
:class:`DepenedentParameter() <ansys.optislang.core.project_parametric.DepenedentParameter>` 
classes with detailed information and simplified method 
:func:`get_parameters_names() <ansys.optislang.core.project_parametric.ParameterManager.get_parameters_names>`, 
that returns tuple of only parameters names.

.. code:: python
    
    parameter_manager = root_system.parameter_manager
    parameters = parameter_manager.get_parameters()
    parameters_names = parameter.get_parameters_names()


When the :class:`Optislang() <ansys.optislang.core.optislang.Optislang>` instance is no longer 
needed, terminate connection with optiSLang server by running:

.. code:: python

    osl.dispose()



