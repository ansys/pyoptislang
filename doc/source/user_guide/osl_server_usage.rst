.. _ref_osl_server_usage:

===================================================
Direct communication using the optiSLang server API
===================================================

PyOptiSLang is intended to provide a Pythonic API on top of Ansys optiSLang.
However, not each and every functionality available through the Ansys optiSLang
server API is already exposed via explicit PyOptiSLang API functionality.

The :class:`TcpOslServer <ansys.optislang.core.tcp_osl_server.TcpOslServer>` wrapper class
can be used for raw communication with optiSLang, in order to overcome this limitation.
It provides explicit methods for accessing specific optiSLang API endpoints. Additionally, the generic
:func:`TcpOslServer.send_command <ansys.optislang.core.tcp_osl_server.TcpOslServer.send_command>` method
can be used in conjunction with the convenience functions from the :ref:`server_queries <ref_osl_server_api_queries>` and
:ref:`server_commands <ref_osl_server_api_commands>` modules.

.. note::

    Please note, that direct communication with Ansys optiSLang server API is discouraged
    for productive usage, as this API and underlying technology is subject to change.
    Please prefer using explicit PyOptiSLang API functionality wherever possible.

You can either directly create an instance of
:class:`TcpOslServer <ansys.optislang.core.tcp_osl_server.TcpOslServer>` class
to connect to an already running instance of optiSLang or just use the
:func:`Optislang.get_osl_server <ansys.optislang.core.optislang.Optislang.get_osl_server>` method
to obtain a handle to the TcpOslServer used by the :class:`Optislang <ansys.optislang.core.optislang.Optislang>`
instance internally. Subsequently, the :class:`TcpOslServer <ansys.optislang.core.tcp_osl_server.TcpOslServer>` class
methods can be used to access the optiSLang server:

.. code:: python

    from ansys.optislang.core import Optislang
    from ansys.optislang.core.project_parametric import Design
    from ansys.optislang.core import examples
    from pathlib import Path

    # open project with defined parameters
    parametric_project = examples.get_files("calculator_with_params")[1][0]
    osl = Optislang(project_path=parametric_project)

    # Query basic server/project info.
    print(f"Basic project info: {osl.get_osl_server().get_basic_project_info()}")
    print(f"Project description: {osl.get_osl_server().get_project_description()}")
    print(f"Project file location: {osl.get_osl_server().get_project_location()}")
    print(f"Project working directory: {osl.get_osl_server().get_working_dir()}")
    print(f"Project name: {osl.get_osl_server().get_project_name()}")
    print(f"Project (run) status: {osl.get_osl_server().get_project_status()}")
    print(f"Full project tree: {osl.get_osl_server().get_full_project_tree()}")

For any optiSLang server API functionality not yet directly exposed in :class:`TcpOslServer <ansys.optislang.core.tcp_osl_server.TcpOslServer>` class,
the generic :mod:`TcpOslServer.send_command <ansys.optislang.core.tcp_osl_server.TcpOslServer.send_command>` method can be used.
It takes a generic request string, sends the request to optiSLang server and returns the corresponding response.
As a convenience, the functions from the :ref:`server_queries <ref_osl_server_api_queries>` and
:ref:`server_commands <ref_osl_server_api_commands>` modules can be used to generate the request strings:

.. code:: python

    from ansys.optislang.core import server_commands as commands
    from ansys.optislang.core import server_queries as queries
    from ansys.optislang.core.project_parametric import Parameter

    # Use raw osl server communication to modify the first parameter
    # on project root level.

    # Get the first parameter on project root level
    root_system_uid = osl.project.root_system.uid
    root_system_properties = osl.get_osl_server().send_command(
        queries.actor_properties(uid=root_system_uid)
    )
    root_system_pm_raw = root_system_properties["properties"]["ParameterManager"]

    first_parameter = Parameter.from_dict(root_system_pm_raw["parameter_container"][0])

    # Print out the reference value
    print(
        f'Parameter "{first_parameter.name}" reference value: {first_parameter.reference_value}'
    )

    # Modify the reference value
    first_parameter.reference_value = 15.0

    # Adapt the parameter manager to the changes and
    # send the modified parameter manager back to optiSLang
    root_system_pm_raw["parameter_container"][0] = first_parameter.to_dict()

    server_response = osl.get_osl_server().send_command(
        commands.set_actor_property(
            actor_uid=root_system_uid, name="ParameterManager", value=root_system_pm_raw
        )
    )

    print(f'Modifying parameter reference value: {server_response[0]["status"]}')

    # Get and print the (now modified) first parameter on project root level
    root_system_properties = osl.get_osl_server().send_command(
        queries.actor_properties(uid=root_system_uid)
    )
    root_system_pm_raw = root_system_properties["properties"]["ParameterManager"]

    modified_first_parameter = Parameter.from_dict(
        root_system_pm_raw["parameter_container"][0]
    )

    print(
        f'Modified parameter "{modified_first_parameter.name}" reference value: {modified_first_parameter.reference_value}'
    )