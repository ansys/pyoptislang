"""Module for generation of all server queries."""
import json
from typing import Any, Dict, Optional

QueryArgs = Dict[str, Any]

_ACTOR_INFO = "ACTOR_INFO"
_ACTOR_PROPERTIES = "ACTOR_PROPERTIES"
_ACTOR_STATES = "ACTOR_STATES"
_ACTOR_STATUS_INFO = "ACTOR_STATUS_INFO"
_ACTOR_SUPPORTS = "ACTOR_SUPPORTS"
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
    password : str, opt
        Password.

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
    password : str, opt
        Password.

    Returns
    -------
    str
        JSON string of actor_properties query.
    """
    return _to_json(_gen_query(what=_ACTOR_PROPERTIES, uid=uid, password=password))


def actor_states(
    uid: str,
    include_state_info: bool = True,
    password: Optional[str] = None,
) -> str:
    """Generate JSON string of actor_states query.

    Parameters
    ----------
    uid: str
        Uid entry.
    include_state_info: bool
        Include additional info for each state. Otherwise, only state IDs are returned.
    password : str, opt
        Password.

    Returns
    -------
    str
        JSON string of actor_states query.
    """
    args: QueryArgs = {}
    args["include_state_info"] = include_state_info
    return _to_json(_gen_query(what=_ACTOR_STATES, uid=uid, args=args, password=password))


def actor_status_info(
    uid: str,
    hid: str,
    include_designs: bool = True,
    include_non_scalar_design_values: bool = False,
    include_algorithm_info: bool = False,
    password: Optional[str] = None,
) -> str:
    """Generate JSON string of actor_status_info query.

    Parameters
    ----------
    uid: str
        Uid entry.
    hid: str
        Hid entry.
    include_designs: bool
        Include (result) designs in status info response.
    include_non_scalar_design_values: bool
        Include non scalar values in (result) designs.
    include_algorithm_info: bool
        Include algorithm result info in status info response.
    password : str, opt
        Password.

    Returns
    -------
    str
        JSON string of actor_status_info query.
    """
    args: QueryArgs = {}
    args["include_designs"] = include_designs
    args["include_non_scalar_design_values"] = include_non_scalar_design_values
    args["include_algorithm_info"] = include_algorithm_info
    return _to_json(
        _gen_query(what=_ACTOR_STATUS_INFO, uid=uid, args=args, hid=hid, password=password)
    )


def actor_supports(uid: str, feature_name: str, password=None) -> str:
    """Generate JSON string of actor_supports query.

    Parameters
    ----------
    uid: str
        Uid entry.
    feature_name: str
        Name of requested feature.
    password : str, opt
        Password.

    Returns
    -------
    str
        JSON string of actor_supports query.
    """
    args: QueryArgs = {}
    args["feature"] = feature_name
    return _to_json(_gen_query(what=_ACTOR_SUPPORTS, uid=uid, args=args, password=password))


def basic_project_info(password: Optional[str] = None) -> str:
    """Generate JSON string of basic_project_info query.

    Parameters
    ----------
    password : str, opt
        Password.

    Returns
    -------
    str
        JSON string of basic_project_info query.
    """
    return _to_json(_gen_query(what=_BASIC_PROJECT_INFO, password=password))


def full_project_status_info(
    include_non_scalar_design_values: bool = False,
    include_algorithm_info: bool = False,
    password: Optional[str] = None,
) -> str:
    """Generate JSON string of full_project_status_info query.

    Parameters
    ----------
    include_non_scalar_design_values: bool
        Include non scalar values in (result) designs.
    include_algorithm_info: bool
        Include algorithm result info in status info response.
    password : str, opt
        Password.

    Returns
    -------
    str
        JSON string of full_project_status_info query.
    """
    args: QueryArgs = {}
    args["include_non_scalar_design_values"] = include_non_scalar_design_values
    args["include_algorithm_info"] = include_algorithm_info
    return _to_json(_gen_query(what=_FULL_PROJECT_STATUS_INFO, args=args, password=password))


def full_project_tree(password: Optional[str] = None) -> str:
    """Generate JSON string of full_project_tree query.

    Parameters
    ----------
    password : str, opt
        Password.

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
    password : str, opt
        Password.

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
    hid: str
        Hid entry.
    slot_name: str
        Slot name entry.
    password : str, opt
        Password.

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
    password : str, opt
        Password.

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
    password : str, opt
        Password.

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
    password : str, opt
        Password.

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
    password : str, opt
        Password.

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
    password : str, opt
        Password.

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
    password : str, opt
        Password.

    Returns
    -------
    str
        JSON string of server_is_alive query.
    """
    return _to_json(_gen_query(what=_SERVER_IS_ALIVE, password=password))


def systems_status_info(
    include_designs: bool = True,
    include_non_scalar_design_values: bool = False,
    include_algorithm_info: bool = False,
    password: Optional[str] = None,
) -> str:
    """Generate JSON string of systems_status_info query.

    Parameters
    ----------
    include_designs: bool
        Include (result) designs in status info response.
    include_non_scalar_design_values: bool
        Include non scalar values in (result) designs.
    include_algorithm_info: bool
        Include algorithm result info in status info response.
    password : str, opt
        Password.

    Returns
    -------
    str
        JSON string of systems_status_info query.
    """
    args: QueryArgs = {}
    args["include_designs"] = include_designs
    args["include_non_scalar_design_values"] = include_non_scalar_design_values
    args["include_algorithm_info"] = include_algorithm_info
    return _to_json(_gen_query(what=_SYSTEMS_STATUS_INFO, args=args, password=password))


def _gen_query(
    what: str,
    password: Optional[str] = None,
    uid: Optional[str] = None,
    hid: Optional[str] = None,
    args: Optional[QueryArgs] = None,
    slot_name: Optional[str] = None,
) -> Dict:
    """Generate query in desired format.

    Parameters
    ----------
    what : str
        Command type.
    password: str
        Password.
    uid : str, optional
        Uid entry.
    hid: str, optional
        Hid entry.
    args: Dict, optional
        Dictionary of features, e.g. "feature": "FEATURE_NAME".
    Returns
    -------
    Dict
        Dictionary with specified query inputs.
    """
    query: Dict[str, Any] = {}
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
