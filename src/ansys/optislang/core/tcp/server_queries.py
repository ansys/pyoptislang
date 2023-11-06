"""Module for generation of all server queries."""
import json
from typing import Dict, Optional

_ACTOR_INFO = "ACTOR_INFO"
_ACTOR_PROPERTIES = "ACTOR_PROPERTIES"
_ACTOR_STATES = "ACTOR_STATES"
_ACTOR_STATUS_INFO = "ACTOR_STATUS_INFO"
_ACTOR_SUPPORTS = "ACTOR_SUPPORTS"
_AVAILABLE_NODES = "AVAILABLE_NODES"
_BASIC_PROJECT_INFO = "BASIC_PROJECT_INFO"
_FULL_PROJECT_STATUS_INFO = "FULL_PROJECT_STATUS_INFO"
_FULL_PROJECT_TREE = "FULL_PROJECT_TREE"
_FULL_PROJECT_TREE_WITH_PROPERTIES = "FULL_PROJECT_TREE_WITH_PROPERTIES"
_HPC_LICENSING_FORWARDED_ENVIRONMENT = "HPC_LICENSING_FORWARDED_ENVIRONMENT"
_INPUT_SLOT_VALUE = "INPUT_SLOT_VALUE"
_OUTPUT_SLOT_VALUE = "OUTPUT_SLOT_VALUE"
_PROJECT_TREE_SYSTEMS = "PROJECT_TREE_SYSTEMS"
_PROJECT_TREE_SYSTEMS_WITH_PROPERTIES = "PROJECT_TREE_SYSTEMS_WITH_PROPERTIES"
_SERVER_INFO = "SERVER_INFO"
_SERVER_IS_ALIVE = "SERVER_IS_ALIVE"
_SYSTEMS_STATUS_INFO = "SYSTEMS_STATUS_INFO"


def actor_info(uid: str, password: Optional[str] = None) -> str:
    """Generate JSON string of actor_info query.

    Parameters
    ----------
    uid: str
        Uid entry.
    password : Optional[str], optional
        Password, by default ``None``.

    Returns
    -------
    str
        JSON string of actor_info query.
    """
    return _to_json(_gen_query(what=_ACTOR_INFO, uid=uid, password=password))


def actor_properties(uid: str, password: Optional[str] = None) -> str:
    """Generate JSON string of actor_properties query.

    Parameters
    ----------
    uid: str
        Uid entry.
    password : Optional[str], optional
        Password, by default ``None``.

    Returns
    -------
    str
        JSON string of actor_properties query.
    """
    return _to_json(_gen_query(what=_ACTOR_PROPERTIES, uid=uid, password=password))


def actor_states(uid: str, password: Optional[str] = None) -> str:
    """Generate JSON string of actor_states query.

    Parameters
    ----------
    uid: str
        Uid entry.
    password : Optional[str], optional
        Password, by default ``None``.

    Returns
    -------
    str
        JSON string of actor_states query.
    """
    return _to_json(_gen_query(what=_ACTOR_STATES, uid=uid, password=password))


def actor_status_info(uid: str, hid: str, password: Optional[str] = None) -> str:
    """Generate JSON string of actor_status_info query.

    Parameters
    ----------
    uid: str
        Uid entry.
    hid: str
        Hid entry.
    password : Optional[str], optional
        Password, by default ``None``.

    Returns
    -------
    str
        JSON string of actor_status_info query.
    """
    return _to_json(_gen_query(what=_ACTOR_STATUS_INFO, uid=uid, hid=hid, password=password))


def actor_supports(uid: str, feature_name: str, password: Optional[str] = None) -> str:
    """Generate JSON string of actor_supports query.

    Parameters
    ----------
    uid: str
        Uid entry.
    feature_name: str
        Name of requested feature.
    password : Optional[str], optional
        Password, by default ``None``.

    Returns
    -------
    str
        JSON string of actor_supports query.
    """
    args = {}
    args["feature"] = feature_name
    return _to_json(_gen_query(what=_ACTOR_SUPPORTS, uid=uid, args=args, password=password))


def available_nodes(password: Optional[str] = None) -> str:
    """Generate JSON string of available nodes query.

    Parameters
    ----------
    password : Optional[str], optional
        Password, by default ``None``.

    Returns
    -------
    str
        JSON string of available nodes query.
    """
    return _to_json(_gen_query(what=_AVAILABLE_NODES, password=password))


def basic_project_info(password: Optional[str] = None) -> str:
    """Generate JSON string of basic_project_info query.

    Parameters
    ----------
    password : Optional[str], optional
        Password, by default ``None``.

    Returns
    -------
    str
        JSON string of available nodes query.
    """
    return _to_json(_gen_query(what=_AVAILABLE_NODES, password=password))


def basic_project_info(password: Optional[str] = None) -> str:
    """Generate JSON string of basic_project_info query.

    Parameters
    ----------
    password : Optional[str], optional
        Password, by default ``None``.

    Returns
    -------
    str
        JSON string of basic_project_info query.
    """
    return _to_json(_gen_query(what=_BASIC_PROJECT_INFO, password=password))


def full_project_status_info(password: Optional[str] = None) -> str:
    """Generate JSON string of full_project_status_info query.

    Parameters
    ----------
    password : Optional[str], optional
        Password, by default ``None``.

    Returns
    -------
    str
        JSON string of full_project_status_info query.
    """
    return _to_json(_gen_query(what=_FULL_PROJECT_STATUS_INFO, password=password))


def full_project_tree(password: Optional[str] = None) -> str:
    """Generate JSON string of full_project_tree query.

    Parameters
    ----------
    password : Optional[str], optional
        Password, by default ``None``.

    Returns
    -------
    str
        JSON string of full_project_tree query.
    """
    return _to_json(_gen_query(what=_FULL_PROJECT_TREE, password=password))


def full_project_tree_with_properties(password: Optional[str] = None) -> str:
    """Generate JSON string of full_project_tree_with_properties query.

    Parameters
    ----------
    password : Optional[str], optional
        Password, by default ``None``.

    Returns
    -------
    str
        JSON string of full_project_tree_with_properties query.
    """
    return _to_json(_gen_query(what=_FULL_PROJECT_TREE_WITH_PROPERTIES, password=password))


def hpc_licensing_forwarded_environment(uid: str, password: Optional[str] = None) -> str:
    """Generate JSON string of hpc_licensing_forwarded_environment query.

    Parameters
    ----------
    uid: str
        Uid entry.
    password : Optional[str], optional
        Password, by default ``None``.

    Returns
    -------
    str
        JSON string of hpc_licensing_forwarded_environment query.
    """
    return _to_json(
        _gen_query(what=_HPC_LICENSING_FORWARDED_ENVIRONMENT, uid=uid, password=password)
    )


def input_slot_value(uid: str, hid: str, slot_name: str, password: Optional[str] = None) -> str:
    """Generate JSON string of input_slot_value query.

    Parameters
    ----------
    uid: str
        Uid entry.
    hid: str
        Hid entry.
    slot_name: str
        Slot name entry.
    password : Optional[str], optional
        Password, by default ``None``.

    Returns
    -------
    str
        JSON string of input_slot_value query.
    """
    return _to_json(
        _gen_query(what=_INPUT_SLOT_VALUE, uid=uid, hid=hid, slot_name=slot_name, password=password)
    )


def output_slot_value(uid: str, hid: str, slot_name: str, password: Optional[str] = None) -> str:
    """Generate JSON string of output_slot_value query.

    Parameters
    ----------
    uid: str
        Uid entry.
    hid: str
        Hid entry.
    slot_name: str
        Slot name entry.
    password : Optional[str], optional
        Password, by default ``None``.

    Returns
    -------
    str
        JSON string of output_slot_value query.
    """
    return _to_json(
        _gen_query(
            what=_OUTPUT_SLOT_VALUE, uid=uid, hid=hid, slot_name=slot_name, password=password
        )
    )


def project_tree_systems(password: Optional[str] = None) -> str:
    """Generate JSON string of project_tree_systems query.

    Parameters
    ----------
    password : Optional[str], optional
        Password, by default ``None``.

    Returns
    -------
    str
        JSON string of project_tree_systems query.
    """
    return _to_json(_gen_query(what=_PROJECT_TREE_SYSTEMS, password=password))


def project_tree_systems_with_properties(password: Optional[str] = None) -> str:
    """Generate JSON string of project_tree_with_properties query.

    Parameters
    ----------
    password : Optional[str], optional
        Password, by default ``None``.

    Returns
    -------
    str
        JSON string of project_tree_with_properties query.
    """
    return _to_json(_gen_query(what=_PROJECT_TREE_SYSTEMS_WITH_PROPERTIES, password=password))


def server_info(password: Optional[str] = None) -> str:
    """Generate JSON string of server_info query.

    Parameters
    ----------
    password : Optional[str], optional
        Password, by default ``None``.

    Returns
    -------
    str
        JSON string of server_info query.
    """
    return _to_json(_gen_query(what=_SERVER_INFO, password=password))


def server_is_alive(password: Optional[str] = None) -> str:
    """Generate JSON string of server_is_alive query.

    Parameters
    ----------
    password : Optional[str], optional
        Password, by default ``None``.

    Returns
    -------
    str
        JSON string of server_is_alive query.
    """
    return _to_json(_gen_query(what=_SERVER_IS_ALIVE, password=password))


def systems_status_info(password: Optional[str] = None) -> str:
    """Generate JSON string of systems_status_info query.

    Parameters
    ----------
    password : Optional[str], optional
        Password, by default ``None``.

    Returns
    -------
    str
        JSON string of systems_status_info query.
    """
    return _to_json(_gen_query(what=_SYSTEMS_STATUS_INFO, password=password))


def _gen_query(
    what: str,
    password: str,
    uid: Optional[str] = None,
    hid: Optional[str] = None,
    args: Optional[Dict] = None,
    slot_name: Optional[str] = None,
) -> Dict:
    """Generate query in desired format.

    Parameters
    ----------
    what : str
        Command type.
    password: str
        Password.
    uid : Optional[str], optional
        Uid entry, by default ``None``.
    hid: Optional[str], optional
        Hid entry, by default ``None``.
    args: Optional[Dict], optional
        Dictionary of features, e.g. "feature": "FEATURE_NAME", by default ``None``.
    slot_name: Optional[str], optional
        Slot name, by default ``None``.
    Returns
    -------
    Dict
        Dictionary with specified query inputs.
    """
    query = {}
    query["What"] = what
    if uid is not None:
        query["uid"] = uid
    if hid is not None:
        query["hid"] = hid
    if args is not None:
        query["args"] = {}
        for feature, feature_name in args.items():
            query["args"][feature] = feature_name
    if slot_name is not None:
        query["slot_name"] = slot_name
    if password is not None:
        query["Password"] = password
    return query


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