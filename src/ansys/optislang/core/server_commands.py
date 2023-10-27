"""Module for generation of all server commands."""
import json
from typing import Dict, Iterable, Sequence, Union

_APPLY_WIZARD = "APPLY_WIZARD"
_CLOSE = "CLOSE"
_CONNECT_NODES = "CONNECT_NODES"
_CREATE_INPUT_SLOT = "CREATE_INPUT_SLOT"
_CREATE_NODE = "CREATE_NODE"
_CREATE_OUTPUT_SLOT = "CREATE_OUTPUT_SLOT"
_CREATE_START_DESIGNS = "CREATE_START_DESIGNS"
_DISCONNECT_SLOT = "DISCONNECT_SLOT"
_EVALUATE_DESIGN = "EVALUATE_DESIGN"
_EXPORT_DESIGNS = "EXPORT_DESIGNS"
_FINALIZE = "FINALIZE"
_LINK_REGISTERED_FILE = "LINK_REGISTERED_FILE"
_NEW = "NEW"
_OPEN = "OPEN"
_PAUSE = "PAUSE"
_REEVALUATE_STATE = "REEVALUATE_STATE"
_REFRESH_LISTENER_REGISTRATION = "REFRESH_LISTENER_REGISTRATION"
_REGISTER_FILE = "REGISTER_FILE"
_REGISTER_LISTENER = "REGISTER_LISTENER"
_REGISTER_LOCATIONS_AS_PARAMETER = "REGISTER_LOCATIONS_AS_PARAMETER"
_REGISTER_LOCATIONS_AS_RESPONSE = "REGISTER_LOCATIONS_AS_RESPONSE"
_REMOVE_NODE = "REMOVE_NODE"
_RE_REGISTER_LOCATIONS_AS_PARAMETER = "RE_REGISTER_LOCATIONS_AS_PARAMETER"
_RE_REGISTER_LOCATIONS_AS_RESPONSE = "RE_REGISTER_LOCATIONS_AS_RESPONSE"
_RESET = "RESET"
_RESTART = "RESTART"
_RESUME = "RESUME"
_RUN_PYTHON_SCRIPT = "RUN_PYTHON_SCRIPT"
_RUN_REGISTERED_FILES_ACTIONS = "RUN_REGISTERED_FILES_ACTIONS"
_SAVE = "SAVE"
_SAVE_AS = "SAVE_AS"
_SAVE_COPY = "SAVE_COPY"
_SET_ACTOR_PROPERTY = "SET_ACTOR_PROPERTY"
_SET_ACTOR_SETTING = "SET_ACTOR_SETTING"
_SET_ACTOR_STATE_PROPERTY = "SET_ACTOR_STATE_PROPERTY"
_SET_PLACEHOLDER_VALUE = "SET_PLACEHOLDER_VALUE"
_SET_PROJECT_SETTING = "SET_PROJECT_SETTING"
_SET_REGISTERED_FILE_VALUE = "SET_REGISTERED_FILE_VALUE"
_SET_START_DESIGNS = "SET_START_DESIGNS"
_SET_SUCCEEDED_STATE = "SET_SUCCEEDED_STATE"
_SHOW_DIALOG = "SHOW_DIALOG"
_SHOW_NODE_DIALOG = "SHOW_NODE_DIALOG"
_SHUTDOWN = "SHUTDOWN"
_SHUTDOWN_WHEN_FINISHED = "SHUTDOWN_WHEN_FINISHED"
_START = "START"
_STOP = "STOP"
_STOP_GENTLY = "STOP_GENTLY"
_SUBSCRIBE_FOR_PUSH_NOTIFICATIONS = "SUBSCRIBE_FOR_PUSH_NOTIFICATIONS"
_UNLINK_REGISTERED_FILE = "UNLINK_REGISTERED_FILE"
_UNREGISTER_FILE = "UNREGISTER_FILE"
_UNREGISTER_LISTENER = "UNREGISTER_LISTENER"
_WRITE_MONITORING_DATABASE = "WRITE_MONITORING_DATABASE"
_builtin = "builtin"


def apply_wizard(
    actor_uid: str,
    type_: str,
    use_existing_system: bool = None,
    usage_mode: str = None,
    parent_hwnd: str = None,
    password: str = None,
) -> str:
    """Generate JSON string of apply_wizzard command.

    Parameters
    ----------
    actor_uid: str
        Unique identifying actor of the object.
    type_: str
        Node or system type, supported values are:
        ["solver", "sensitivity", "optimization", "robustness", "reevaluation"].
    use_existing_system: bool, opt
        True or false.
    usage_mode: str, opt
        Usage mode, e.g. "EXPERT".
    parent_hwnd: str, opt
        Parent hwnd.
    password : str, opt
        Password.

    Returns
    -------
    str
        JSON string of apply_wizzard command.
    """
    args = {}
    supported_values = ["solver", "sensitivity", "optimization", "robustness", "reevaluation"]
    if type_ in supported_values:
        args["type"] = type_
    else:
        raise TypeError(
            f"Unsuppored value of ``type_``: {type_}, supported values are: {supported_values}"
        )
    if use_existing_system is not None:
        args["use_existing_system"] = use_existing_system
    if usage_mode is not None:
        args["usage_mode"] = usage_mode
    # TODO: and/or:  The request must contain the actor_uid entry as well as the args entry,
    # containing the argument type and optionally the arguments usage_mode,
    # use_existing_system and/or parent_hwnd."
    if parent_hwnd is not None:
        args["parent_hwnd"] = parent_hwnd

    return _to_json(
        _gen_server_command(
            command=_APPLY_WIZARD, actor_uid=actor_uid, args=args, password=password
        )
    )


def close(password: str = None) -> str:
    """Generate JSON string of close command.

    Parameters
    ----------
    password : str, opt
        Password.

    Returns
    -------
    str
        JSON string of close command.
    """
    return _to_json(_gen_server_command(command=_CLOSE, password=password))


def connect_nodes(
    from_actor_uid: str, from_slot: str, to_actor_uid: str, to_slot: str, password: str = None
) -> str:
    """Generate JSON string of connect_nodes command.

    Parameters
    ----------
    from_actor_uid: str
        Uid of connection source.
    from_slot: str
        Slot of connection source.
    to_actor_uid: str
        Uid of connection target.
    to_slot: str
        Slot of connection target.
    password : str, opt
        Password.

    Returns
    -------
    str
        JSON string of connect_nodes command.
    """
    args = {}
    args["from_actor_uid"] = from_actor_uid
    args["from_slot"] = from_slot
    args["to_actor_uid"] = to_actor_uid
    args["to_slot"] = to_slot

    return _to_json(_gen_server_command(command=_CONNECT_NODES, args=args, password=password))


def create_input_slot(
    actor_uid: str, slot_name: str, type_hint: str = None, password: str = None
) -> str:
    """Generate JSON string of create_input_slot command.

    Parameters
    ----------
    actor_uid: str
        Actor uid entry.
    slot_name: str
        Name of slot.
    type_hint: str, opt
        Type of hint.
    password : str, opt
        Password.

    Returns
    -------
    str
        JSON string of create_input_slot command.
    """
    args = {}
    args["slot_name"] = slot_name
    if type_hint is not None:
        args["type_hint"] = type_hint

    return _to_json(
        _gen_server_command(
            command=_CREATE_INPUT_SLOT, actor_uid=actor_uid, args=args, password=password
        )
    )


def create_node(
    type_: str, name: str, parent_uid: str = None, design_flow: str = None, password: str = None
) -> str:
    """Generate JSON string of create_node command.

    Parameters
    ----------
    type_: str
        Type.
    name: str
        Name.
    parent_uid: str, opt
        Parent uid entry.
    design_flow: str, opt
        Design flow, optional values are ["RECEIVE", "SEND", "RECEIVE_SEND"].
    password : str, opt
        Password.

    Returns
    -------
    str
        JSON string of create_node command.
    """
    args = {}
    args["type"] = type_
    args["name"] = name
    if parent_uid is not None:
        args["parent_uid"] = parent_uid
    if design_flow not in [None, "NONE"]:
        args["design_flow"] = design_flow

    return _to_json(_gen_server_command(command=_CREATE_NODE, args=args, password=password))


def create_output_slot(
    actor_uid: str, slot_name: str, type_hint: str = None, password: str = None
) -> str:
    """Generate JSON string of create_output_slot command.

    Parameters
    ----------
    actor_uid: str
        Actor uid entry.
    slot_name: str
        Name of the slot.
    type_hint: str
        Type of the hint.
    password : str, opt
        Password.

    Returns
    -------
    str
        JSON string of create_output_slot command.
    """
    args = {}
    args["slot_name"] = slot_name
    if type_hint is not None:
        args["type_hint"] = type_hint
    return _to_json(
        _gen_server_command(
            command=_CREATE_OUTPUT_SLOT, actor_uid=actor_uid, args=args, password=password
        )
    )


def create_start_designs(
    actor_uid: str,
    sampling_type: str,
    number_of_levels: int = None,
    number_of_samples: int = None,
    password: str = None,
) -> str:
    """Generate JSON string of create_start_design command.

    Parameters
    ----------
    actor_uid: str
        Actor uid entry.
    sampling_type: str
        Sampling type, e.g. "fullfactorial".
    number_of_levels: int, opt
        Number of levels.
    number_of_samples: int, opt
        Number of samples.
    password : str, opt
        Password.

    Returns
    -------
    str
        JSON string of create_start_design command.
    """
    args = {}
    args["sampling_type"] = sampling_type
    if (number_of_levels is not None) and (number_of_samples is not None):
        raise TypeError(f"Please specify either ``number_of_levels`` or ``number of samples``.")
    elif number_of_levels is not None:
        args["number_of_levels"] = number_of_levels
    elif number_of_samples is not None:
        args["number_of_samples"] = number_of_samples

    return _to_json(
        _gen_server_command(
            command=_CREATE_START_DESIGNS, actor_uid=actor_uid, args=args, password=password
        )
    )


def disconnect_slot(actor_uid: str, slot_name: str, direction: str, password: str = None) -> str:
    """Generate JSON string of disconnect_slot command.

    Parameters
    ----------
    actor_uid: str
        Actor uid entry.
    slot_name: str
        Name of the slot.
    direction: str
        Direction.
    password : str, opt
        Password.

    Returns
    -------
    str
        JSON string of disconnect_slot command.
    """
    args = {}
    args["slot_name"] = slot_name
    args["direction"] = direction
    return _to_json(
        _gen_server_command(
            command=_DISCONNECT_SLOT, actor_uid=actor_uid, args=args, password=password
        )
    )


def evaluate_design(parameters: Dict, password: str = None) -> str:
    """Generate JSON string of evaluate_design command.

    Parameters
    ----------
    parameters: Dict
        Dictionary of parameters.
    password : str, opt
        Password.

    Returns
    -------
    str
        JSON string of evaluate_design command.
    """
    args = {}
    args["parameters"] = parameters
    return _to_json(_gen_server_command(command=_EVALUATE_DESIGN, args=args, password=password))


def export_designs(
    actor_uid: str, path: str, format: str = None, csv_separator: str = None, password: str = None
) -> str:
    """Generate JSON string of export_designs command.

    Parameters
    ----------
    actor_uid: str
        Actor uid entry.
    path: str
       Path.
    format: str, opt
        Type_hint format.
    csv_separator: str, opt
        CSV separator.
    password : str, opt
        Password.

    Returns
    -------
    str
        JSON string of export_designs command.
    """
    args = {}
    args["path"] = path
    if format is not None:
        args["format"] = format
    if csv_separator is not None:
        args["csv_separator"] = csv_separator

    return _to_json(
        _gen_server_command(
            command=_EXPORT_DESIGNS, actor_uid=actor_uid, args=args, password=password
        )
    )


def finalize(actor_uid: str, password: str = None) -> str:
    """Generate JSON string of finalize command.

    Parameters
    ----------
    actor_uid: str
        Actor uid entry.
    password : str, opt
        Password.

    Returns
    -------
    str
        JSON string of finalize command.
    """
    return _to_json(_gen_server_command(command=_FINALIZE, actor_uid=actor_uid, password=password))


def link_registered_file(actor_uid: str, uid: str, password: str = None) -> str:
    """Generate JSON string of link_registered_file command.

    Parameters
    ----------
    actor_uid: str
        Actor uid entry.
    uid: str
        Uid entry.
    password : str, opt
        Password.

    Returns
    -------
    str
        JSON string of link_registered_file command.
    """
    args = {}
    args["uid"] = uid
    return _to_json(
        _gen_server_command(
            command=_LINK_REGISTERED_FILE, actor_uid=actor_uid, args=args, password=password
        )
    )


def new(password: str = None) -> str:
    """Generate JSON string of ``new`` command.

    Parameters
    ----------
    password : str, opt
        Password.

    Returns
    -------
    str
        JSON string of ``new`` command.
    """
    return _to_json(_gen_server_command(command=_NEW, password=password))


def open(path: str, do_force: bool, do_restore: bool, do_reset: bool, password: str = None) -> str:
    """Generate JSON string of ``open`` command.

    Parameters
    ----------
    path: str
        path.
    do_force: bool
        True/False.
    do_restore: bool
        True/False.
    do_reset: bool
        True/False.
    password : str, opt
        Password.

    Returns
    -------
    str
        JSON string of ``open`` command.
    """
    args = {}
    args["path"] = path
    args["do_force"] = do_force
    args["do_restore"] = do_restore
    args["do_reset"] = do_reset

    return _to_json(_gen_server_command(command=_OPEN, args=args, password=password))


def pause(password: str = None) -> str:
    """Generate JSON string of pause command.

    Parameters
    ----------
    password : str, opt
        Password.

    Returns
    -------
    str
        JSON string of pause command.
    """
    return _to_json(_gen_server_command(command=_PAUSE, password=password))


def reevaluate_state(actor_uid: str, hid: str = None, password: str = None) -> str:
    """Generate JSON string of reevaluate_state command.

    Parameters
    ----------
    actor_uid: str
        Actor uid entry.
    hid: str
        Hid entry.
    password : str, opt
        Password.

    Returns
    -------
    str
        JSON string of reevaluate_state command.
    """
    return _to_json(
        _gen_server_command(
            command=_REEVALUATE_STATE, actor_uid=actor_uid, hid=hid, password=password
        )
    )


def refresh_listener_registration(uid: str, password: str = None) -> str:
    """Generate JSON string of refresh_listener_registration command.

    Parameters
    ----------
    uid: str
        Uid entry.
    password : str, opt
        Password.

    Returns
    -------
    str
        JSON string of refresh_listener_registration command.
    """
    args = {}
    args["uid"] = uid
    return _to_json(
        _gen_server_command(command=_REFRESH_LISTENER_REGISTRATION, args=args, password=password)
    )


def register_file(
    uid: str = None,
    ident: str = None,
    local_location: Dict = None,
    action: str = None,
    password: str = None,
) -> str:
    """Generate JSON string of register_file command.

    Parameters
    ----------
    uid: str, opt
        Uid entry.
    ident: str, opt
        Ident.
    local_location: Dict, opt
        Dictionary specifying location, e. g. { "split_path": {"head": "",
        "tail": "C:/samples_path/result.txt" }, "base_path": "",
        "base_path_mode": "ABSOLUTE_PATH" }.
    action: str, opt
        Action, e. g. "Send"
    password : str, opt
        Password.

    Returns
    -------
    str
        JSON string of register_file command.
    """
    # TODO: "and so on: specify all possibilities"
    args = {}
    if uid is not None:
        args["uid"] = uid
    if ident is not None:
        args["ident"] = ident
    if local_location is not None:
        args["local_location"] = local_location
    if action is not None:
        args["action"] = action

    return _to_json(_gen_server_command(command=_REGISTER_FILE, args=args, password=password))


def register_listener(
    id: str = None,
    host: str = None,
    port: int = None,
    timeout: int = None,
    notifications: Iterable[str] = None,
    password: str = None,
    listener_uid: str = None,
) -> str:
    """Generate JSON string of register_listener command.

    Parameters
    ----------
    id: str, opt
        Id of the local listener.
    host: str, opt
        IP of the TCP listener
    port: int, opt
        Port of the TCP listener.
    time_out: int, opt
        Unregister policy timeout in ms, default 60000 ms.
    notifications: Sequence, opt
        Notifications.
    password : str, opt
        Password.
    listener_uid : str, opt
        Listener UID.

    Returns
    -------
    str
        JSON string of register_listener command.
    """
    args = {}
    if (id is not None) and ((host is not None) or (port is not None)):
        raise TypeError(f"Please specify either ``id`` or (``host`` and ``port``).")
    elif (id is None) and ((host is None) or (port is None)):
        raise TypeError(f"Please specify either ``id`` or (``host`` and ``port``).")
    elif id is not None:
        args["id"] = id
    else:
        args["host"] = host
        args["port"] = port

    if timeout is not None:
        args["timeout"] = timeout
    if notifications is not None:
        args["notifications"] = notifications
    if listener_uid is not None:
        args["uid"] = listener_uid

    return _to_json(_gen_server_command(command=_REGISTER_LISTENER, args=args, password=password))


def register_locations_as_parameter(actor_uid: str, password: str = None) -> str:
    """Generate JSON string of ``register_location_as_parameter`` command.

    Parameters
    ----------
    actor_uid: str
        Actor uid entry.
    password : str, opt
        Password.

    Returns
    -------
    str
        JSON string of ``register_location_as_parameter`` command.
    """
    return _to_json(
        _gen_server_command(
            command=_REGISTER_LOCATIONS_AS_PARAMETER, actor_uid=actor_uid, password=password
        )
    )


def register_locations_as_response(actor_uid: str, password: str = None) -> str:
    """Generate JSON string of ``register_location_as_response`` command.

    Parameters
    ----------
    actor_uid: str
        Actor uid entry.
    password : str, opt
        Password.

    Returns
    -------
    str
        JSON string of ``register_location_as_response`` command.
    """
    return _to_json(
        _gen_server_command(
            command=_REGISTER_LOCATIONS_AS_RESPONSE, actor_uid=actor_uid, password=password
        )
    )


def remove_node(actor_uid: str, password: str = None) -> str:
    """Generate JSON string of ``remove node`` command.

    Parameters
    ----------
    actor_uid: str
        Actor uid entry.
    password : str, opt
        Password.

    Returns
    -------
    str
        JSON string of ``remove_node`` command.
    """
    return _to_json(
        _gen_server_command(command=_REMOVE_NODE, actor_uid=actor_uid, password=password)
    )


def re_register_locations_as_parameter(actor_uid: str, password: str = None) -> str:
    """Generate JSON string of ``re_register_locations_as_parameter`` command.

    Parameters
    ----------
    actor_uid: str
        Actor uid entry.
    password : str, opt
        Password.

    Returns
    -------
    str
        JSON string of ``re_register_locations_as_parameter`` command.
    """
    return _to_json(
        _gen_server_command(
            command=_RE_REGISTER_LOCATIONS_AS_PARAMETER, actor_uid=actor_uid, password=password
        )
    )


def re_register_locations_as_response(actor_uid: str, password: str = None) -> str:
    """Generate JSON string of ``re_register_locations_as_response`` command.

    Parameters
    ----------
    actor_uid: str
        Actor uid entry.
    password : str, opt
        Password.

    Returns
    -------
    str
        JSON string of ``re_register_locations_as_response`` command.
    """
    return _to_json(
        _gen_server_command(
            command=_RE_REGISTER_LOCATIONS_AS_RESPONSE, actor_uid=actor_uid, password=password
        )
    )


def reset(actor_uid: str = None, hid: str = None, password: str = None) -> str:
    """Generate JSON string of ``reset`` command.

    Parameters
    ----------
    actor_uid: str, opt
        Actor uid entry. A Hirearchical ID (hid) is required.
    hid: str, opt
        Hid entry. The actor uid is required.
    password : str, opt
        Password.

    Returns
    -------
    str
        JSON string of ``reset`` command.
    """
    if actor_uid and hid is None:
        raise ValueError("The Hirearchical ID (hid) is required.")
    elif actor_uid is None and hid:
        raise ValueError("The actor uid is required.")
    return _to_json(
        _gen_server_command(command=_RESET, actor_uid=actor_uid, hid=hid, password=password)
    )


def restart(actor_uid: str = None, hid: str = None, password: str = None) -> str:
    """Generate JSON string of ``restart`` command.

    Parameters
    ----------
    actor_uid: str, opt
        Actor uid entry. A Hirearchical ID (hid) is required.
    hid: str, opt
        Hid entry. The actor uid is required.
    password : str, opt
        Password.

    Returns
    -------
    str
        JSON string of ``restart`` command.
    """
    if actor_uid and hid is None:
        raise ValueError("The Hirearchical ID (hid) is required.")
    elif actor_uid is None and hid:
        raise ValueError("The actor uid is required.")
    return _to_json(
        _gen_server_command(command=_RESTART, actor_uid=actor_uid, hid=hid, password=password)
    )


def resume(password: str = None) -> str:
    """Generate JSON string of ``resume`` command.

    Parameters
    ----------
    password : str, opt
        Password.

    Returns
    -------
    str
        JSON string of ``resume`` command.
    """
    return _to_json(_gen_server_command(command=_RESUME, password=password))


def run_python_script(
    script: str,
    args_: list = None,
    password: str = None,
) -> str:
    """Generate JSON string of register_listener command.

    Parameters
    ----------
    script: str
        Path of the script.
    args: list, opt
        IP of the TCP listener.
    password : str, opt
        Password.

    Returns
    -------
    str
        JSON string of register_listener command.
    """
    args = {}
    args["script"] = script
    if args_ is not None:
        args["args"] = args_

    return _to_json(_gen_server_command(command=_RUN_PYTHON_SCRIPT, args=args, password=password))


def run_registered_files_actions(
    uid: str = None,
    password: str = None,
) -> str:
    """Generate JSON string of ``run registered files actions`` command.

    Parameters
    ----------
    uid: str, opt
        Uid entry.
    password : str, opt
        Password.

    Returns
    -------
    str
        JSON string of ``run registered files actions`` command.
    """
    args = None
    if uid is not None:
        args = {}
        args["uid"] = uid

    return _to_json(
        _gen_server_command(command=_RUN_REGISTERED_FILES_ACTIONS, args=args, password=password)
    )


def save(password: str = None) -> str:
    """Generate JSON string of ``save`` command.

    Parameters
    ----------
    password : str, opt
        Password.

    Returns
    -------
    str
        JSON string of ``save`` command.
    """
    return _to_json(_gen_server_command(command=_SAVE, password=password))


def save_as(
    path: str, do_force: bool, do_restore: bool, do_reset: bool, password: str = None
) -> str:
    """Generate JSON string of ``save_as`` command.

    Parameters
    ----------
    path: str
        path.
    do_force: bool
        True/False.
    do_restore: bool
        True/False.
    do_reset: bool
        True/False.
    password : str, opt
        Password.

    Returns
    -------
    str
        JSON string of ``save_as`` command.
    """
    args = {}
    args["path"] = path
    args["do_force"] = do_force
    args["do_restore"] = do_restore
    args["do_reset"] = do_reset

    return _to_json(_gen_server_command(command=_SAVE_AS, args=args, password=password))


def save_copy(path: str, password: str = None) -> str:
    """Generate JSON string of ``save_copy`` command.

    Parameters
    ----------
    path: str
        path.
    password : str, opt
        Password.

    Returns
    -------
    str
        JSON string of ``save_copy`` command.
    """
    args = {}
    args["path"] = path

    return _to_json(_gen_server_command(command=_SAVE_COPY, args=args, password=password))


def set_actor_property(actor_uid: str, name: str, value: str, password: str = None) -> str:
    """Generate JSON string of ``set_actor_property`` command.

    Parameters
    ----------
    actor_uid: str
        Actor uid entry.
    name: str
        Property name.
    value: str
        Value.
    password : str, opt
        Password.

    Returns
    -------
    str
        JSON string of ``set_actor_property`` command.
    """
    args = {}
    args["name"] = name
    args["value"] = value

    return _to_json(
        _gen_server_command(
            command=_SET_ACTOR_PROPERTY, actor_uid=actor_uid, args=args, password=password
        )
    )


def set_actor_setting(actor_uid: str, name: str, value: str, password: str = None) -> str:
    """Generate JSON string of ``set actor setting`` command.

    Parameters
    ----------
    actor_uid: str
        Actor uid entry.
    name: str
        Property name.
    value: str
        Value.
    password : str, opt
        Password.

    Returns
    -------
    str
        JSON string of ``set actor setting`` command.
    """
    args = {}
    args["name"] = name
    args["value"] = value

    return _to_json(
        _gen_server_command(
            command=_SET_ACTOR_SETTING, actor_uid=actor_uid, args=args, password=password
        )
    )


def set_actor_state_property(actor_uid: str, name: str, value: str, password: str = None) -> str:
    """Generate JSON string of ``set actor state property`` command.

    Parameters
    ----------
    actor_uid: str
        Actor uid entry.
    name: str
        Property name.
    value: str
        Value.
    password : str, opt
        Password.

    Returns
    -------
    str
        JSON string of ``set actor state property`` command.
    """
    args = {}
    args["name"] = name
    args["value"] = value

    return _to_json(
        _gen_server_command(
            command=_SET_ACTOR_STATE_PROPERTY, actor_uid=actor_uid, args=args, password=password
        )
    )


def set_placeholder_value(name: str, value: str, password: str = None) -> str:
    """Generate JSON string of ``set placeholder value`` command.

    Parameters
    ----------
    name: str
        Property name.
    value: str
        Value.
    password : str, opt
        Password.

    Returns
    -------
    str
        JSON string of ``set placeholder value`` command.
    """
    args = {}
    args["name"] = name
    args["value"] = value

    return _to_json(
        _gen_server_command(command=_SET_PLACEHOLDER_VALUE, args=args, password=password)
    )


def set_project_setting(name: str, value: str, password: str = None) -> str:
    """Generate JSON string of ``set project settings`` command.

    Parameters
    ----------
    name: str
        Property name.
    value: str
        Value.
    password : str, opt
        Password.

    Returns
    -------
    str
        JSON string of ``set project settings`` command.
    """
    args = {}
    args["name"] = name
    args["value"] = value

    return _to_json(_gen_server_command(command=_SET_PROJECT_SETTING, args=args, password=password))


def set_registered_file_value(
    uid: str, name: str, value: Union[str, Dict], password: str = None
) -> str:
    """Generate JSON string of ``set registered file value`` command.

    Parameters
    ----------
    uid: str
        Uid entry.
    name: str
        Property name.
    value: Union[str, Dict]
        Value.
    password : str, opt
        Password.

    Returns
    -------
    str
        JSON string of ``set registered file value`` command.
    """
    args = {}
    args["uid"] = uid
    args["name"] = name
    args["value"] = value

    return _to_json(
        _gen_server_command(command=_SET_REGISTERED_FILE_VALUE, args=args, password=password)
    )


def set_start_designs(actor_uid: str, start_designs: Dict, password: str = None) -> str:
    """Generate JSON string of ``set start designs`` command.

    Parameters
    ----------
    actor_uid: str
        Actor uid entry.
    start_designs: Dict
        Dictionary of settings.
    password : str, opt
        Password.

    Returns
    -------
    str
        JSON string of ``set start designs`` command.
    """
    # TODO: function to create start_settings?
    args = {}
    args["start_designs"] = start_designs

    return _to_json(
        _gen_server_command(
            command=_SET_START_DESIGNS, actor_uid=actor_uid, args=args, password=password
        )
    )


def set_succeeded_state(actor_uid: str, hid: str = None, password: str = None) -> str:
    """Generate JSON string of ``set succeeded state`` command.

    Parameters
    ----------
    actor_uid: str
        Actor uid entry.
    hid: str, opt
        Hid entry.
    password : str, opt
        Password.

    Returns
    -------
    str
        JSON string of ``set succeeded state`` command.
    """
    return _to_json(
        _gen_server_command(
            command=_SET_SUCCEEDED_STATE, actor_uid=actor_uid, hid=hid, password=password
        )
    )


def show_dialog(
    type_: str, usage_mode: str = None, parent_hwnd: str = None, password: str = None
) -> str:
    """Generate JSON string of ``show dialog`` command.

    Parameters
    ----------
    type_: str
        Argument type,
        for application dialogs: [ "about", "help", "settings", "plugin" ]
        for project dialogs: [ "project_settings", "project_overview", "license_management",
        "registered_files", "purge", "load_from", "save_to" ].
    usage_mode: str, opt
        Usage mode. e.g. "EXPERT".
    parent_hwnd: str, opt
        Parent hwnd.
    password : str, opt
        Password.

    Returns
    -------
    str
        JSON string of ``show dialog`` command.
    """
    application_dialogs = ["about", "help", "settings", "plugin"]
    project_dialogs = [
        "project_settings",
        "project_overview",
        "license_management",
        "registered_files",
        "purge",
        "load_from",
        "save_to",
    ]

    if not ((type_ in application_dialogs) or (type_ in project_dialogs)):
        raise TypeError(
            f"Unsuppored value of ``type_``: {type_}, supported values for application dialogs: "
            "{application_dialogs} and for project dialogs: {project_dialogs}"
        )
    args = {}
    args["type"] = type_
    if usage_mode is not None:
        args["usage_mode"] = usage_mode
    if parent_hwnd is not None:
        args["parent_hwnd"] = parent_hwnd

    return _to_json(_gen_server_command(command=_SHOW_DIALOG, args=args, password=password))


def show_node_dialog(
    actor_uid: str,
    blocking: bool = None,
    type_: str = None,
    usage_mode: str = None,
    parent_hwnd: str = None,
    password: str = None,
) -> str:
    """Generate JSON string of ``show node dialog`` command.

    Parameters
    ----------
    actor_uid: str
        Actor uid entry.
    blocking: bool, opt
        True/False.
    type_: str, opt
        Type, e.g. "help".
    usage_mode: str, opt
        Usage mode. e.g. "EXPERT".
    parent_hwnd: str, opt
        Parent hwnd.
    password : str, opt
        Password.

    Returns
    -------
    str
        JSON string of ``show node dialog`` command.
    """
    args = None
    if not (
        (blocking is None) and (type_ is None) and (usage_mode is None) and (parent_hwnd is None)
    ):
        args = {}
        if blocking is not None:
            args["blocking"] = blocking
        if type_ is not None:
            args["type"] = type_
        if usage_mode is not None:
            args["usage_mode"] = usage_mode
        if parent_hwnd is not None:
            args["parent_hwnd"] = parent_hwnd

    return _to_json(
        _gen_server_command(
            command=_SHOW_NODE_DIALOG, actor_uid=actor_uid, args=args, password=password
        )
    )


def shutdown(password: str = None) -> str:
    """Generate JSON string of ``shutdown`` command.

    Parameters
    ----------
    password : str, opt
        Password.

    Returns
    -------
    str
        JSON string of ``shutdown`` command.
    """
    return _to_json(_gen_server_command(command=_SHUTDOWN, password=password))


def shutdown_when_finished(password: str = None) -> str:
    """Generate JSON string of ``shutdown_when_finished`` command.

    Parameters
    ----------
    password : str, opt
        Password.

    Returns
    -------
    str
        JSON string of ``shutdown_when_finished`` command.
    """
    return _to_json(_gen_server_command(command=_SHUTDOWN_WHEN_FINISHED, password=password))


def start(actor_uid: str = None, hid: str = None, password: str = None) -> str:
    """Generate JSON string of ``start`` command.

    Parameters
    ----------
    actor_uid: str, opt
        Actor uid entry. A Hirearchical ID (hid) is required.
    hid: str, opt
        Hid entry. The actor uid is required.
    password : str, opt
        Password.

    Returns
    -------
    str
        JSON string of ``start`` command.
    """
    if actor_uid and hid is None:
        raise ValueError("The Hirearchical ID (hid) is required.")
    elif actor_uid is None and hid:
        raise ValueError("The actor uid is required.")

    return _to_json(
        _gen_server_command(command=_START, actor_uid=actor_uid, hid=hid, password=password)
    )


def stop(actor_uid: str = None, hid: str = None, password: str = None) -> str:
    """Generate JSON string of ``stop`` command.

    Parameters
    ----------
    actor_uid: str, opt
        Actor uid entry. A Hirearchical ID (hid) is required.
    hid: str, opt
        Hid entry. The actor uid is required.
    password : str, opt
        Password.

    Returns
    -------
    str
        JSON string of ``stop`` command.
    """
    if actor_uid and hid is None:
        raise ValueError("The Hirearchical ID (hid) is required.")
    elif actor_uid is None and hid:
        raise ValueError("The actor uid is required.")

    return _to_json(
        _gen_server_command(command=_STOP, actor_uid=actor_uid, hid=hid, password=password)
    )


def stop_gently(actor_uid: str = None, hid: str = None, password: str = None) -> str:
    """Generate JSON string of ``stop_gently`` command.

    Parameters
    ----------
    actor_uid: str, opt
        Actor uid entry. A Hirearchical ID (hid) is required.
    hid: str, opt
        Hid entry. The actor uid is required.
    password : str, opt
        Password.

    Returns
    -------
    str
        JSON string of ``stop_gently`` command.
    """
    if actor_uid and hid is None:
        raise ValueError("The Hirearchical ID (hid) is required.")
    elif actor_uid is None and hid:
        raise ValueError("The actor uid is required.")
    return _to_json(
        _gen_server_command(command=_STOP_GENTLY, actor_uid=actor_uid, hid=hid, password=password)
    )


def subscribe_for_push_notifications(
    uid: str, notifications: Sequence, node_types: Sequence = None, password: str = None
) -> str:
    """Generate JSON string of ``subscribe_for_push_notifications`` command.

    Parameters
    ----------
    uid: str
        Uid entry.
    notifications: Sequence
        Either ["ALL"] or Sequence picked from below options:
            Server: [ "SERVER_UP", "SERVER_DOWN" ] (always be sent by default).
            Logging: [ "LOG_INFO", "LOG_WARNING", "LOG_ERROR", "LOG_DEBUG" ].
            Project: [ "EXECUTION_STARTED", "PROCESSING_STARTED", "EXECUTION_FINISHED",
            "NOTHING_PROCESSED", "CHECK_FAILED", "EXEC_FAILED" ].
            Nodes: [ "ACTOR_STATE_CHANGED", "ACTOR_ACTIVE_CHANGED", "ACTOR_NAME_CHANGED",
            ACTOR_CONTENTS_CHANGED", "ACTOR_DATA_CHANGED" ].
    node_types: Sequence, opt
       Node types, e.g. ["Sensitivity", "AnsysWorkbench"].
    password : str, opt
        Password.

    Returns
    -------
    str
        JSON string of ``subscribe_for_push_notifications`` command.
    """
    server = ["SERVER_UP", "SERVER_DOWN"]
    logging = ["LOG_INFO", "LOG_WARNING", "LOG_ERROR", "LOG_DEBUG"]
    project = [
        "EXECUTION_STARTED",
        "PROCESSING_STARTED",
        "EXECUTION_FINISHED",
        "NOTHING_PROCESSED",
        "CHECK_FAILED",
        "EXEC_FAILED",
    ]
    nodes = [
        "ACTOR_STATE_CHANGED",
        "ACTOR_ACTIVE_CHANGED",
        "ACTOR_NAME_CHANGED",
        "ACTOR_CONTENTS_CHANGED",
        "ACTOR_DATA_CHANGED",
    ]
    all_opts = set(server + logging + project + nodes)

    args = {}
    args["uid"] = uid

    if notifications == ["ALL"]:
        args["notifications"] = notifications
    else:
        if not all(item in all_opts for item in notifications):
            invalid_items = list(sorted(all_opts - set(notifications)))
            raise TypeError(
                f"Unsuppored values of ``notifications``: {invalid_items}, "
                "supported options are: \n"
                f"server: {server},\n"
                f"logging: {logging},\n"
                f"project: {project},\n"
                f"nodes: {nodes}"
            )
        args["notifications"] = notifications

    if node_types is not None:
        args["node_types"] = node_types

    return _to_json(
        _gen_server_command(command=_SUBSCRIBE_FOR_PUSH_NOTIFICATIONS, args=args, password=password)
    )


def unlink_registered_file(actor_uid: str, uid: str, password: str = None) -> str:
    """Generate JSON string of ``unlink registered file`` command.

    Parameters
    ----------
    actor_uid: str
        Actor uid entry.
    uid: str
        Uid entry.
    password : str, opt
        Password.

    Returns
    -------
    str
        JSON string of ``unlink registered file`` command.
    """
    args = {}
    args["uid"] = uid

    return _to_json(
        _gen_server_command(
            command=_UNLINK_REGISTERED_FILE, actor_uid=actor_uid, args=args, password=password
        )
    )


def unregister_file(uid: str, password: str = None) -> str:
    """Generate JSON string of ``unregister file`` command.

    Parameters
    ----------
    uid: str
        Uid entry.
    password : str, opt
        Password.

    Returns
    -------
    str
        JSON string of ``unregister file`` command.
    """
    args = {}
    args["uid"] = uid

    return _to_json(_gen_server_command(command=_UNREGISTER_FILE, args=args, password=password))


def unregister_listener(uid: str, password: str = None) -> str:
    """Generate JSON string of ``unregister listener`` command.

    Parameters
    ----------
    uid: str
        Uid entry.
    password : str, opt
        Password.

    Returns
    -------
    str
        JSON string of ``unregister listener`` command.
    """
    args = {}
    args["uid"] = uid

    return _to_json(_gen_server_command(command=_UNREGISTER_LISTENER, args=args, password=password))


def write_monitoring_database(
    actor_uid: str, path: str = None, hid: str = None, password: str = None
) -> str:
    """Generate JSON string of ``write monitoring database`` command.

    Parameters
    ----------
    actor_uid: str
        Actor uid entry.
    path: str, opt
        Path.
    hid: str, opt
        Hid entry.
    password : str, opt
        Password.

    Returns
    -------
    str
        JSON string of ``write monitoring database`` command.
    """
    args = None
    if (path is not None) or (hid is not None):
        args = {}
        if path is not None:
            args["path"] = path
        if hid is not None:
            args["hid"] = hid

    return _to_json(
        _gen_server_command(
            command=_WRITE_MONITORING_DATABASE, actor_uid=actor_uid, args=args, password=password
        )
    )


def _gen_server_command(command, password, args=None, actor_uid=None, hid=None) -> Dict:
    """Generate server command.

    Parameters
    ----------
    command : str
        Command type.
    password : str, opt
        Password.
    args : Dict, opt
        Dictionary with specified arguments.
    actor_uid : str, opt

    Returns
    -------
    scmd : Dict
        Dictionary of server command.

    """
    scmd = {}
    scmd["projects"] = []
    commands = {}
    commands["commands"] = []
    commands["commands"].append(
        _gen_command(command=command, args=args, actor_uid=actor_uid, hid=hid)
    )
    scmd["projects"].append(commands)
    if password:
        scmd["Password"] = password
    return scmd


def _gen_command(command: str, args: Dict = None, actor_uid: str = None, hid: str = None) -> Dict:
    """Generate "commands" for method server command.

    Parameters
    ----------
    type : str
        Command type.
    command : str
        Command name.
    args: dict, optional
        Arguments.
    actor_uid: str, optional
        Actor uid.
    hid: str, optional
        Actor hid.

    Returns
    -------
    dictionary: dict
        Specified dictionary.
    """
    cmd = {}
    cmd["type"] = _builtin
    cmd["command"] = command
    if args:
        cmd["args"] = {}
        for feature, feature_name in args.items():
            cmd["args"][feature] = feature_name
    if actor_uid:
        cmd["actor_uid"] = actor_uid
    if hid:
        cmd["hid"] = hid
    return cmd


def _to_json(dict: Dict) -> str:
    """Convert dictionary to JSON.

    Parameters
    ----------
    dict : Dict
        Dictionary with specified query inputs.

    Returns
    -------
    str
        JSON string.
    """
    return json.dumps(dict, sort_keys=True, ensure_ascii=False)
