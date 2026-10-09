## Workflow Metadata Properties

### `project_settings`

> **On-demand only.** Emit `"project_settings": {}` by default. Only populate specific keys when the user explicitly requests them.

```json
"project_settings": {
    "actors_ignore_predecessor_failure": true,
    "autosave_enabled": true,
    "custom_location": "",
    "edition_feature_consumption_quantity": 1,
    "filename_escape_mode": "full",
    "force_edition_feature_consumption_quantity": false,
    "force_preferred_edition": false,
    "hide_number_of_message_queue_threads_warning": false,
    "license_checkin_after_wf_run": false,
    "maximum_auto_relocation_depth": 3,
    "number_of_message_queue_threads": 0,
    "persistent_heartbeat_listeners": [],
    "preferred_edition": 0,
    "project_actions": [],
    "project_id": "",
    "project_manager_id": "",
    "purge_filter": null,
    "purge_on_save": false,
    "reference_files_delete_on_close": false,
    "reference_files_directory_custom_location": "",
    "reference_files_directory_location_mode": "alongsideproject",
    "reference_files_directory_name": "reffildir",
    "reference_files_directory_storage_mode": "external",
    "remove_empty_directories_on_purge": true,
    "short_description": "",
    "show_conditional_exec_ui": "indeterminate",
    "show_environment_ui": "indeterminate",
    "show_files_ui": "indeterminate",
    "show_placeholders_ui": "indeterminate",
    "show_run_options_ui": "indeterminate",
    "show_variables_ui": "indeterminate",
    "working_data_storage": "external",
    "working_directory_location": "alongsideproject"
}
```

Use `"reference_files_directory_storage_mode": "embedded"` to bundle files inside the WDF for portability.

### `registered_files`

> **On-demand only.** Emit `"registered_files": []` by default. Only add entries when the user explicitly names a file to register.

```json
"registered_files": [
    {
        "action": "None",
        "action_point": "Manual",
        "auto_generated": false,
        "comment": "",
        "embedded": false,
        "existence": "DontCare",
        "external_location": "",
        "filename_regex": "",
        "ident": "my_script",
        "local_location": {
            "base_path_mode": "REFERENCE_FILES_DIR_RELATIVE",
            "split_path": { "head": "", "tail": "my_script.py" }
        },
        "properties": {},
        "remove_on_reset": false,
        "revision": "",
        "type": "Filesystem",
        "usage": "Undetermined",
        "use_regex_for_filename": false,
        "wait_for_file": false
    }
]
```

### `placeholder_*`

> **On-demand only.** Emit `"placeholder_*": {}` by default. Only add entries when the user explicitly defines a placeholder.

```json
"placeholder_definitions" : 
{
    "MaxParallel" : 
    {
        "description" : "",
        "range" : "",
        "type" : "uint",
        "user_level" : "computation_engineer"
    }
},
"placeholder_mapping" : 
{
    "MaxParallel" : 
    {
        "property_key" : "MaxParallel",
        "property_source_path" : "Python"
    }
},
"placeholder_values" : 
{
    "MaxParallel" : 1
}
```
