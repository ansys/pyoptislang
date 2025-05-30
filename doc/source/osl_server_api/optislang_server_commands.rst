.. _ref_osl_server_api_commands:

Server commands
===============
These methods are specific to the :py:mod:`ansys.optislang.core.tcp.server_commands <ansys.optislang.core.tcp.server_commands>` module
and can be used to generate commands to the optiSLang server:

.. currentmodule:: ansys.optislang.core.tcp.server_commands

.. autosummary::
   :toctree: _autosummary

   apply_wizard
   add_criterion
   close
   connect_nodes
   create_input_slot
   create_node
   create_output_slot
   create_start_designs
   disconnect_nodes
   disconnect_slot
   evaluate_design
   export_designs
   finalize
   link_registered_file
   load
   new
   open
   pause
   reevaluate_state
   refresh_listener_registration
   register_file
   register_listener
   register_location_as_input_slot
   register_location_as_internal_variable
   register_location_as_output_slot
   register_location_as_parameter
   register_locations_as_parameter
   register_location_as_response
   register_locations_as_response
   remove_criteria
   remove_criterion
   remove_node
   rename_node
   rename_slot
   re_register_locations_as_parameter
   re_register_locations_as_response
   reset
   restart
   resume
   run_python_script
   run_registered_files_actions
   save
   save_as
   save_copy
   set_actor_property
   set_actor_setting
   set_actor_state_property
   set_criterion_property
   set_placeholder_value
   set_project_setting
   set_registered_file_value
   set_start_designs
   set_succeeded_state
   show_dialog
   show_node_dialog
   shutdown
   shutdown_when_finished
   start
   stop
   stop_gently
   subscribe_for_push_notifications
   unlink_registered_file
   unregister_file
   unregister_listener
   write_monitoring_database
