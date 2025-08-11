.. _placeholders_howto:

Working with placeholders
=========================

This guide provides instructions for working with placeholders in optiSLang.

Overview
--------

In optiSlang, placeholders are variables that can be assigned to workflow component (node) properties, allowing you to easily update properties in more than one workflow component at a time. You can also use placeholders to directly expose workflow component properties for external modification (for example, by a user of an optiSLang App or the command line interface).

Each placeholder has the following attributes:

- **ID**: A unique identifier for the placeholder
- **Data Type**: Specifies what kind of data the placeholder can hold (string, real number, boolean, etc.)
- **User Level**: Controls which user roles can modify the placeholder
- **Description**: Optional documentation about the placeholder's purpose

Depending on the desired use case, placeholders can either store fixed values or be composed out of other placeholders via a macro expression. The respective attributes are:

- **Value**: The current value stored in the placeholder
- **Range**: The range of allowed values
- **Macro Expression**: The macro expression defining the placeholder's composition. See "Placeholder Macro Language" in the optiSLang documentation for more information.

API capabilities for managing placeholders include:

- Creating placeholders with specific data types and user access levels
- Assigning values appropriate to their data type
- Querying and filtering by ID patterns
- Renaming and removing
- Assigning to and unassigning from node properties

The API supports both project-level operations (via :py:class:`Project <ansys.optislang.core.project.Project>` class) for managing placeholders globally and node-level operations (via :py:class:`Node <ansys.optislang.core.nodes.Node>` class) for creating placeholders from node properties and managing assignments to them.

Creating placeholders
---------------------

Placeholders are intended to be values stored separately from the workflow components in the project and then assigned to one or multiple workflow component properties.
Creating placeholders can be achieved by either creating a stand-alone (unassigned) one (via :py:meth:`create_placeholder() <ansys.optislang.core.project.Project.create_placeholder>`) and then assign it to a workflow component property (via :py:meth:`assign_placeholder() <ansys.optislang.core.nodes.Node.assign_placeholder>`) or directly creating the placeholder from a workflow component property (via via :py:meth:`create_placeholder_from_property() <ansys.optislang.core.nodes.Node.create_placeholder_from_property>`).

Variant 1 - Step 1: Create stand-alone placeholder
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from ansys.optislang.core import Optislang
    from ansys.optislang.core.placeholder_types import PlaceholderType, UserLevel

    # Connect to optiSLang
    osl = Optislang()

    # Create a real number placeholder for thickness
    thickness_id = osl.project.create_placeholder(
        value=5.0,
        placeholder_id="thickness",
        type_=PlaceholderType.REAL,
        user_level=UserLevel.COMPUTATION_ENGINEER,
        description="Plate thickness in mm",
    )

    # Create a string placeholder for material name
    material_id = osl.project.create_placeholder(
        value="Steel",
        placeholder_id="material_name",
        type_=PlaceholderType.STRING,
        user_level=UserLevel.FLOW_ENGINEER,
        description="Material name",
    )

    # Create an integer placeholder for maximum number of parallel executions
    global_max_parallel_id = osl.project.create_placeholder(
        value=8,
        placeholder_id="global_max_parallel",
        type_=PlaceholderType.INT,
        user_level=UserLevel.FLOW_ENGINEER,
        description="Maximum number of parallel executions",
    )

Variant 1 - Step 2: Assigning existing placeholders
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Placeholders are type-specific. A placeholder can be assigned to a project property only if they share the same data type.

.. code-block:: python

    from ansys.optislang.core.placeholder_types import PlaceholderType, UserLevel

    # Get a node reference
    root_system = osl.project.root_system
    mop_solver_node = root_system.create_node(
        type_=node_types.Mopsolver, name="MOPSolver Node"
    )

    # Assign the placeholder to a node property
    mop_solver_node.assign_placeholder(
        property_name="MaxParallel", placeholder_id="max_parallel"
    )

Variant 2: Creating placeholders directly from node properties
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from ansys.optislang.core import node_types

    # Get a node reference
    root_system = osl.project.root_system
    mop_solver_node = root_system.create_node(
        type_=node_types.Mopsolver, name="MOPSolver Node"
    )

    # Create a placeholder from a node property
    placeholder_id = mop_solver_node.create_placeholder_from_property(
        property_name="MaxParallel", placeholder_id="max_parallel"
    )
    print(f"Created placeholder: {placeholder_id}")

    # Create placeholder with auto-generated ID
    auto_id = mop_solver_node.create_placeholder_from_property(property_name="RetryCount")
    print(f"Auto-generated placeholder ID: {auto_id}")

Creating placeholders with macro expressions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

optiSLang allows you to define macro expressions. Macro expressions create placeholder values composed of other user-defined placeholders or predefined constants. By using macro expressions, complex workflow component properties like algorithm systems parametric can be assembled out of separate placeholder values for e.g parameter reference values or ranges. The separate placeholders can then be configured to be accessible externally.
The macro language slightly differs between the types, but all types share the same rules for placeholder substitution, text concatenation, and literal escaping. Please refer to the optiSLang documentation on more information on the macro language syntax.

.. code-block:: python

    # Get a node reference
    root_system = osl.project.root_system
    mop_solver_node = root_system.create_node(
        type_=node_types.Mopsolver, name="MOPSolver Node"
    )

    # Create a placeholder as an expression from a node property. The placeholder will be assigned to the node property. The property value will be used as expression value by default.
    placeholder_id = mop_solver_node.create_placeholder_from_property(
        property_name="MaxParallel", create_as_expression=True
    )
    print(f"Created expression placeholder: {placeholder_id}")

    # You can also directly specify the expression.
    placeholder_id_2 = mop_solver_node.create_placeholder_from_property(
        property_name="MaxParallel", expression="global_max_parallel/2"
    )
    print(f"Created expression placeholder: {placeholder_id_2}")

Unassigning placeholders from nodes
-----------------------------------

Placeholders can be unassigned from node properties when their parameterization is no longer needed by using :py:meth:`unassign_placeholder() <ansys.optislang.core.nodes.Node.unassign_placeholder>`.

.. code-block:: python

    # Unassign a placeholder from a node property
    try:
        calculator_node.unassign_placeholder(property_name="RetryEnable")
        print("✓ Placeholder unassigned from RetryEnable property")
    except Exception as e:
        print(f"✗ Failed to unassign placeholder: {e}")


Querying placeholders
---------------------

You can query existing placeholders to retrieve information about their configuration by using :py:meth:`get_placeholder_ids() <ansys.optislang.core.project.Project.get_placeholder_ids>` and :py:meth:`get_placeholder() <ansys.optislang.core.project.Project.get_placeholder>`.

Getting all placeholder IDs
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    # Get all placeholder IDs in the project
    placeholder_ids = osl.project.get_placeholder_ids()

    print(f"Found {len(placeholder_ids)} placeholders:")
    for placeholder_id in placeholder_ids:
        print(f"  - {placeholder_id}")

Getting placeholder information
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    # Get detailed information about a specific placeholder
    placeholder_info = osl.project.get_placeholder("thickness")

    print(f"Placeholder ID: {placeholder_info.placeholder_id}")
    print(f"Type: {placeholder_info.type}")
    print(f"User Level: {placeholder_info.user_level}")
    print(f"Description: {placeholder_info.description}")
    print(f"Current Value: {placeholder_info.value}")

    # Get information about all placeholders
    placeholder_ids = osl.project.get_placeholder_ids()
    for placeholder_id in placeholder_ids:
        info = osl.project.get_placeholder(placeholder_id)
        print(f"ID: {info.placeholder_id}, Type: {info.type}, Value: {info.value}")

Editing placeholder configuration and setting values
----------------------------------------------------

After creating placeholders, you can modify their configuration by using :py:meth:`create_placeholder() <ansys.optislang.core.project.Project.create_placeholder>` again and specifying the ``overwrite`` argument.
As a convenience you can use :py:meth:`set_placeholder_value() <ansys.optislang.core.project.Project.set_placeholder_value>` to set their values specifically.

.. code-block:: python

    # Modify one or multiple configuration entries of a placeholder
    osl.project.create_placeholder(
        placeholder_id="global_max_parallel",
        value=18,
        description="Adapted description for maximum number of parallel executions",
        overwrite=True,
    )

    # Set a placeholder value specifically
    osl.project.set_placeholder_value("thickness", 7.5)

Validating placeholder updates
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    # Set a value and verify it was updated
    new_value = 8.5
    osl.project.set_placeholder_value("thickness", new_value)

    # Verify the update
    placeholder_info = osl.project.get_placeholder("thickness")
    current_value = placeholder_info.value

    if current_value == new_value:
        print(f"✓ Successfully updated thickness to {new_value}")
    else:
        print(f"✗ Update failed. Expected {new_value}, got {current_value}")

Renaming placeholders
---------------------

Placeholders can be renamed while preserving their values and assignments by using :py:meth:`rename_placeholder() <ansys.optislang.core.project.Project.rename_placeholder>`.

.. code-block:: python

    # Rename a placeholder
    old_id = "thickness"
    new_id = "plate_thickness"
    try:
        osl.project.rename_placeholder(old_id, new_id)
        print(f"✓ Renamed '{old_id}' to '{new_id}'")
    except Exception as e:
        print(f"Failed to rename placeholder: {e}")

Removing placeholders
---------------------

Placeholders can be removed from the project when no longer needed by using :py:meth:`remove_placeholder() <ansys.optislang.core.project.Project.remove_placeholder>`.

.. code-block:: python

    # Remove a placeholder by ID
    try:
        osl.project.remove_placeholder("plate_thickness")
        print("Placeholder removed successfully")
    except Exception as e:
        print(f"Failed to remove placeholder: {e}")
