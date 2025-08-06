.. _placeholders_howto:

Working with Placeholders
=========================

This guide provides comprehensive instructions for working with placeholders in the optiSLang Python API. Placeholders are named parameters that can be used throughout your optiSLang project to parameterize models and analyses.

Overview
--------

Placeholders in optiSLang serve as named parameters that can store values of different data types and can be used throughout your optiSLang project to parameterize models and analyses. Each placeholder has:

- **Data Type**: Specifies what kind of data the placeholder can hold (string, real number, boolean, etc.)
- **User Level**: Controls which user roles can modify the placeholder
- **Value**: The current value stored in the placeholder
- **Range**: The range of allowed values
- **Description**: Optional documentation about the placeholder's purpose
- **Macro Expression**: Instead of storing a fixed value, a placeholder can be composed out of other placeholders via a macro expression

Placeholders can be:

- Created with specific data types and user access levels
- Assigned values appropriate to their data type
- Queried and filtered by ID patterns
- Renamed and removed
- Assigned to and unassigned from node properties

The API supports both project-level operations for managing placeholders globally and node-level operations for creating placeholders from node properties and managing assignments to them.

Creating Placeholders
---------------------

Creating placeholders requires specifying a value, data type, and user level using the appropriate enums.

Basic Example
~~~~~~~~~~~~~

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
        description="Plate thickness in mm"
    )
    
    # Create a string placeholder for material name
    material_id = osl.project.create_placeholder(
        value="Steel",
        placeholder_id="material_name",
        type_=PlaceholderType.STRING,
        user_level=UserLevel.FLOW_ENGINEER,
        description="Material name"
    )
    
    # Create a boolean placeholder for optimization flag
    optimization_flag = osl.project.create_placeholder(
        value=True,
        placeholder_id="enable_optimization",
        type_=PlaceholderType.BOOL,
        user_level=UserLevel.COMPUTATION_ENGINEER,
        description="Enable optimization process"
    )
    
    # Create an integer placeholder for iteration count
    max_iter_id = osl.project.create_placeholder(
        value=100,
        placeholder_id="max_iterations",
        type_=PlaceholderType.INT,
        user_level=UserLevel.FLOW_ENGINEER,
        description="Maximum number of iterations"
    )

Querying Placeholders
---------------------

You can query existing placeholders to retrieve information about their properties, values, and assignments.

Getting All Placeholder IDs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    # Get all placeholder IDs in the project
    placeholder_ids = osl.project.get_placeholder_ids()
    
    print(f"Found {len(placeholder_ids)} placeholders:")
    for placeholder_id in placeholder_ids:
        print(f"  - {placeholder_id}")

Getting Placeholder Information
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

Setting Placeholder Values
--------------------------

After creating placeholders, you can set their values using the available API methods.

.. code-block:: python

    # Set a placeholder value
    osl.project.set_placeholder_value("thickness", 7.5)
    
    # Set different types of values
    osl.project.set_placeholder_value("material_name", "Steel")
    osl.project.set_placeholder_value("use_optimization", True)
    osl.project.set_placeholder_value("load_factor", 1.25)

Validating Placeholder Updates
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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

Renaming Placeholders
---------------------

Placeholders can be renamed while preserving their values and assignments.

.. code-block:: python

    # Rename a placeholder
    try:
        osl.project.rename_placeholder("old_name", "new_name")
        print("Placeholder renamed successfully")
    except Exception as e:
        print(f"Failed to rename placeholder: {e}")

    # Rename with validation
    old_id = "thickness"
    new_id = "plate_thickness"
    
    # Check if old placeholder exists
    placeholder_ids = osl.project.get_placeholder_ids()
    if old_id in placeholder_ids:
        try:
            osl.project.rename_placeholder(old_id, new_id)
            print(f"✓ Renamed '{old_id}' to '{new_id}'")
        except Exception as e:
            print(f"✗ Rename failed: {e}")
    else:
        print(f"✗ Placeholder '{old_id}' does not exist")

Removing Placeholders
---------------------

Placeholders can be removed from the project when no longer needed.

.. code-block:: python

    # Remove a placeholder by ID
    try:
        osl.project.remove_placeholder("unused_parameter")
        print("Placeholder removed successfully")
    except Exception as e:
        print(f"Failed to remove placeholder: {e}")

    # Remove with existence check
    placeholder_id = "old_placeholder"
    placeholder_ids = osl.project.get_placeholder_ids()
    
    if placeholder_id in placeholder_ids:
        try:
            osl.project.remove_placeholder(placeholder_id)
            print(f"✓ Removed placeholder '{placeholder_id}'")
        except Exception as e:
            print(f"✗ Failed to remove '{placeholder_id}': {e}")
    else:
        print(f"Placeholder '{placeholder_id}' does not exist")

Assigning Placeholders to Nodes
-------------------------------

Placeholders can be assigned to specific node properties in your optiSLang workflow to parameterize their behavior.

Creating Placeholders from Node Properties
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from ansys.optislang.core import node_types

    # Get a node reference
    root_system = osl.project.root_system
    calculator_node = root_system.create_node(
        type_=node_types.CalculatorSet, 
        name="Calculator"
    )
    
    # Create a placeholder from a node property
    placeholder_id = calculator_node.create_placeholder_from_property(
        property_name="RetryEnable",
        placeholder_id="retry_enabled"
    )
    print(f"Created placeholder: {placeholder_id}")
    
    # Create placeholder with auto-generated ID
    auto_id = calculator_node.create_placeholder_from_property(
        property_name="MaxIterations"
    )
    print(f"Auto-generated placeholder ID: {auto_id}")

Creating Expression Placeholders
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    # Create a placeholder as an expression from a node property
    expression_id = calculator_node.create_placeholder_from_property(
        property_name="RetryEnable",
        placeholder_id="retry_expression",
        create_as_expression=True
    )
    print(f"Created expression placeholder: {expression_id}")

Assigning Existing Placeholders
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from ansys.optislang.core.placeholder_types import PlaceholderType, UserLevel

    # First create a boolean placeholder
    placeholder_id = osl.project.create_placeholder(
        value=True,
        placeholder_id="global_retry_flag",
        type_=PlaceholderType.BOOL,
        user_level=UserLevel.COMPUTATION_ENGINEER,
        description="Global retry flag for all calculations"
    )
    
    # Assign the placeholder to a node property
    calculator_node.assign_placeholder(
        property_name="RetryEnable",
        placeholder_id="global_retry_flag"
    )
    print("Placeholder assigned to node property")

Unassigning Placeholders from Nodes
-----------------------------------

Placeholders can be unassigned from node properties when their parameterization is no longer needed.

.. code-block:: python

    # Unassign a placeholder from a node property
    try:
        calculator_node.unassign_placeholder(property_name="RetryEnable")
        print("✓ Placeholder unassigned from RetryEnable property")
    except Exception as e:
        print(f"✗ Failed to unassign placeholder: {e}")
