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


Project structure
-----------------
The optiSLang project can be represented by a rooted tree structure. This structure consists 
of nodes and connections between them. On the top level, there is one node designated as a project 
root system which is represented by the :class:`RootSystem() <ansys.optislang.core.nodes.RootSystem>` 
instance. Each :class:`System() <ansys.optislang.core.nodes.System>`
(for example :class:`RootSystem() <ansys.optislang.core.nodes.RootSystem>`, 
:class:`ParametricSystem() <ansys.optislang.core.nodes.ParametricSystem>`) has a method 
:func:`get_nodes() <ansys.optislang.core.nodes.get_nodes>` which returns all its direct children 
nodes. This provides an ability to determine whole project structure. The example below shows 
how to go through all nodes in the project and print information about them.

.. code:: python

    # ...

    def print_node_info(node):
        name = node.get_name()
        type_ = node.get_type()
        status = node.get_status()
        print(name, type_, status)


    def process_nodes(nodes):
        for node in nodes:
            print_node_info(node)
            if isinstance(node, System):
                process_nodes(node.get_nodes())


    root_system = project.root_system
    nodes = root_system.get_nodes()
    process_nodes(nodes)


Parameters
----------
In order to obtain defined parameters of any parametric system, instance of the 
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
    
    # ...

    parameter_manager = root_system.parameter_manager
    parameters = parameter_manager.get_parameters()
    parameters_names = parameter.get_parameters_names()


When the :class:`Optislang() <ansys.optislang.core.optislang.Optislang>` instance is no longer 
needed, terminate connection with optiSLang server by running:

.. code:: python

    osl.dispose()



