"Module for testing server_queries.py"
import json

import pytest

from ansys.optislang.core import tcp_server_queries as sq

my_string = "5cdfb20b-bef6-4412-9985-89f5ded5ee95"
my_dict = {"feature": "CAN_FINALIZE"}
hid = "0.1"
my_slot = "MySlot"
my_password = "otislang.-*123"


def test_actor_info():
    "Test actor_info."
    json_string = sq.actor_info(uid=my_string)
    dictionary = json.loads(json_string)
    requiered_string = json.loads(
        '{ "What": "ACTOR_INFO", "uid": "5cdfb20b-bef6-4412-9985-89f5ded5ee95" }'
    )
    assert type(json_string) == str
    assert sorted(dictionary.items()) == sorted(requiered_string.items())
    # with password
    json_string = sq.actor_info(uid=my_string, password=my_password)
    dictionary = json.loads(json_string)
    dictionary["Password"] = my_password
    with pytest.raises(TypeError):
        sq.actor_info()


def test_actor_properties():
    "Test actor_properties."
    json_string = sq.actor_properties(uid=my_string)
    dictionary = json.loads(json_string)
    requiered_string = json.loads(
        '{ "What": "ACTOR_PROPERTIES", "uid": "5cdfb20b-bef6-4412-9985-89f5ded5ee95" }'
    )
    assert type(json_string) == str
    assert sorted(dictionary.items()) == sorted(requiered_string.items())
    # with password
    json_string = sq.actor_properties(uid=my_string, password=my_password)
    dictionary = json.loads(json_string)
    dictionary["Password"] = my_password
    with pytest.raises(TypeError):
        sq.actor_properties()


def test_actor_states():
    "Test actor_states."
    json_string = sq.actor_states(uid=my_string)
    dictionary = json.loads(json_string)
    requiered_string = json.loads(
        '{ "What": "ACTOR_STATES", "uid": "5cdfb20b-bef6-4412-9985-89f5ded5ee95" }'
    )
    assert type(json_string) == str
    assert sorted(dictionary.items()) == sorted(requiered_string.items())
    # with password
    json_string = sq.actor_states(uid=my_string, password=my_password)
    dictionary = json.loads(json_string)
    dictionary["Password"] = my_password
    with pytest.raises(TypeError):
        sq.actor_states()


def test_actor_status_info():
    "Test actor_status_info."
    json_string = sq.actor_status_info(uid=my_string, hid=hid)
    dictionary = json.loads(json_string)
    requiered_string = json.loads(
        '{ "What": "ACTOR_STATUS_INFO", "uid": "5cdfb20b-bef6-4412-9985-89f5ded5ee95",'
        ' "hid": "0.1" }',
    )
    assert type(json_string) == str
    assert sorted(dictionary.items()) == sorted(requiered_string.items())
    # with password
    json_string = sq.actor_status_info(uid=my_string, hid=hid, password=my_password)
    dictionary = json.loads(json_string)
    dictionary["Password"] = my_password
    with pytest.raises(TypeError):
        sq.actor_status_info()
    with pytest.raises(TypeError):
        sq.actor_status_info(uid=my_string)
    with pytest.raises(TypeError):
        sq.actor_status_info(hid=my_string)


def test_actor_supports():
    "Test actor_supports."
    json_string = sq.actor_supports(uid=my_string, feature_name="CAN_FINALIZE")
    dictionary = json.loads(json_string)
    requiered_string = json.loads(
        '{ "What": "ACTOR_SUPPORTS", "uid": "5cdfb20b-bef6-4412-9985-89f5ded5ee95",'
        ' "args": { "feature": "CAN_FINALIZE" } }',
    )
    assert type(json_string) == str
    assert sorted(dictionary.items()) == sorted(requiered_string.items())
    # with password
    json_string = sq.actor_supports(
        uid=my_string, feature_name="CAN_FINALIZE", password=my_password
    )
    dictionary = json.loads(json_string)
    dictionary["Password"] = my_password
    with pytest.raises(TypeError):
        sq.actor_supports()
    with pytest.raises(TypeError):
        sq.actor_supports(uid=my_string)
    with pytest.raises(TypeError):
        sq.actor_supports(args=my_dict)


def test_basic_project_info():
    "Test basic_project_info."
    json_string = sq.basic_project_info()
    dictionary = json.loads(json_string)
    requiered_string = json.loads('{ "What": "BASIC_PROJECT_INFO" }')
    assert type(json_string) == str
    assert sorted(dictionary.items()) == sorted(requiered_string.items())
    # with password
    json_string = sq.basic_project_info(password=my_password)
    dictionary = json.loads(json_string)
    dictionary["Password"] = my_password
    with pytest.raises(TypeError):
        sq.basic_project_info(rand_arg=my_string)


def test_full_project_status_info():
    "Test full_project_status_info."
    json_string = sq.full_project_status_info()
    dictionary = json.loads(json_string)
    requiered_string = json.loads('{ "What": "FULL_PROJECT_STATUS_INFO" }')
    assert type(json_string) == str
    assert sorted(dictionary.items()) == sorted(requiered_string.items())
    # with password
    json_string = sq.full_project_status_info(password=my_password)
    dictionary = json.loads(json_string)
    dictionary["Password"] = my_password
    with pytest.raises(TypeError):
        sq.full_project_status_info(rand_arg=my_string)


def test_full_project_tree():
    "Test full_project_tree."
    json_string = sq.full_project_tree()
    dictionary = json.loads(json_string)
    requiered_string = json.loads('{ "What": "FULL_PROJECT_TREE" }')
    assert type(json_string) == str
    assert sorted(dictionary.items()) == sorted(requiered_string.items())
    # with password
    json_string = sq.full_project_tree(password=my_password)
    dictionary = json.loads(json_string)
    dictionary["Password"] = my_password
    with pytest.raises(TypeError):
        sq.full_project_tree(rand_arg=my_string)


def test_full_project_tree_with_properties():
    "Test full_project_tree_with_properties."
    json_string = sq.full_project_tree_with_properties()
    dictionary = json.loads(json_string)
    requiered_string = json.loads('{ "What": "FULL_PROJECT_TREE_WITH_PROPERTIES" }')
    assert type(json_string) == str
    assert sorted(dictionary.items()) == sorted(requiered_string.items())
    # with password
    json_string = sq.full_project_tree_with_properties(password=my_password)
    dictionary = json.loads(json_string)
    dictionary["Password"] = my_password
    with pytest.raises(TypeError):
        sq.full_project_tree_with_properties(rand_arg=my_string)


def test_hpc_licensing_forwarded_environment():
    "Test hpc_licensing_forwarded_environment."
    json_string = sq.hpc_licensing_forwarded_environment(uid=my_string)
    dictionary = json.loads(json_string)
    requiered_string = json.loads(
        '{ "What": "HPC_LICENSING_FORWARDED_ENVIRONMENT",'
        ' "uid": "5cdfb20b-bef6-4412-9985-89f5ded5ee95" }'
    )
    assert type(json_string) == str
    assert sorted(dictionary.items()) == sorted(requiered_string.items())
    # with password
    json_string = sq.hpc_licensing_forwarded_environment(uid=my_string, password=my_password)
    dictionary = json.loads(json_string)
    dictionary["Password"] = my_password
    with pytest.raises(TypeError):
        sq.hpc_licensing_forwarded_environment()


def test_input_slot_value():
    "Test input slot value."
    json_string = sq.input_slot_value(uid=my_string, hid=hid, slot_name="IDesign")
    dictionary = json.loads(json_string)
    requiered_string = json.loads(
        '{ "What": "INPUT_SLOT_VALUE", "uid": "5cdfb20b-bef6-4412-9985-89f5ded5ee95",'
        ' "hid": "0.1", "slot_name": "IDesign" }'
    )
    assert type(json_string) == str
    assert sorted(dictionary.items()) == sorted(requiered_string.items())
    # with password
    json_string = sq.input_slot_value(
        uid=my_string, hid=hid, slot_name="IDesign", password=my_password
    )
    dictionary = json.loads(json_string)
    dictionary["Password"] = my_password
    with pytest.raises(TypeError):
        sq.input_slot_value()
    with pytest.raises(TypeError):
        sq.input_slot_value(uid=my_string)
    with pytest.raises(TypeError):
        sq.input_slot_value(hid=hid)
    with pytest.raises(TypeError):
        sq.input_slot_value(slot_name=my_slot)
    with pytest.raises(TypeError):
        sq.input_slot_value(hid=hid, slot_name=my_slot)
    with pytest.raises(TypeError):
        sq.input_slot_value(uid=my_string, slot_name=my_slot)
    with pytest.raises(TypeError):
        sq.input_slot_value(uid=my_string, hid=hid)


def test_output_slot_value():
    "Test output slot value."
    json_string = sq.output_slot_value(uid=my_string, hid=hid, slot_name="ODesign")
    dictionary = json.loads(json_string)
    requiered_string = json.loads(
        '{ "What": "OUTPUT_SLOT_VALUE", "uid": "5cdfb20b-bef6-4412-9985-89f5ded5ee95",'
        ' "hid": "0.1", "slot_name": "ODesign" }'
    )
    assert type(json_string) == str
    assert sorted(dictionary.items()) == sorted(requiered_string.items())
    # with password
    json_string = sq.output_slot_value(
        uid=my_string, hid=hid, slot_name="ODesign", password=my_password
    )
    dictionary = json.loads(json_string)
    dictionary["Password"] = my_password
    with pytest.raises(TypeError):
        sq.output_slot_value()
    with pytest.raises(TypeError):
        sq.output_slot_value(uid=my_string)
    with pytest.raises(TypeError):
        sq.output_slot_value(hid=hid)
    with pytest.raises(TypeError):
        sq.output_slot_value(slot_name=my_slot)
    with pytest.raises(TypeError):
        sq.output_slot_value(hid=hid, slot_name=my_slot)
    with pytest.raises(TypeError):
        sq.output_slot_value(uid=my_string, slot_name=my_slot)
    with pytest.raises(TypeError):
        sq.output_slot_value(uid=my_string, hid=hid)


def test_project_tree_systems():
    "Test project_tree_systems."
    json_string = sq.project_tree_systems()
    dictionary = json.loads(json_string)
    requiered_string = json.loads('{ "What": "PROJECT_TREE_SYSTEMS" }')
    assert type(json_string) == str
    assert sorted(dictionary.items()) == sorted(requiered_string.items())
    # with password
    json_string = sq.project_tree_systems(password=my_password)
    dictionary = json.loads(json_string)
    dictionary["Password"] = my_password
    with pytest.raises(TypeError):
        sq.project_tree_systems(rand_arg=my_string)


def test_project_tree_systems_with_properties():
    "Test project_tree_systems_with_properties."
    json_string = sq.project_tree_systems_with_properties()
    dictionary = json.loads(json_string)
    requiered_string = json.loads('{ "What": "PROJECT_TREE_SYSTEMS_WITH_PROPERTIES" }')
    assert type(json_string) == str
    assert sorted(dictionary.items()) == sorted(requiered_string.items())
    # with password
    json_string = sq.project_tree_systems_with_properties(password=my_password)
    dictionary = json.loads(json_string)
    dictionary["Password"] = my_password
    with pytest.raises(TypeError):
        sq.project_tree_systems_with_properties(rand_arg=my_string)


def test_server_info():
    "Test server_info."
    json_string = sq.server_info()
    dictionary = json.loads(json_string)
    requiered_string = json.loads('{ "What": "SERVER_INFO" }')
    assert type(json_string) == str
    assert sorted(dictionary.items()) == sorted(requiered_string.items())
    # with password
    json_string = sq.server_info(password=my_password)
    dictionary = json.loads(json_string)
    dictionary["Password"] = my_password
    with pytest.raises(TypeError):
        sq.server_info(rand_arg=my_string)


def test_server_is_alive():
    "Test server_is_alive."
    json_string = sq.server_is_alive()
    dictionary = json.loads(json_string)
    requiered_string = json.loads('{ "What": "SERVER_IS_ALIVE" }')
    assert type(json_string) == str
    assert sorted(dictionary.items()) == sorted(requiered_string.items())
    # with password
    json_string = sq.server_is_alive(password=my_password)
    dictionary = json.loads(json_string)
    dictionary["Password"] = my_password
    with pytest.raises(TypeError):
        sq.server_is_alive(rand_arg=my_string)


def test_systems_status_info():
    "Test server_status_info."
    json_string = sq.systems_status_info()
    dictionary = json.loads(json_string)
    requiered_string = json.loads('{ "What": "SYSTEMS_STATUS_INFO" }')
    assert type(json_string) == str
    assert sorted(dictionary.items()) == sorted(requiered_string.items())
    # with password
    json_string = sq.systems_status_info(password=my_password)
    dictionary = json.loads(json_string)
    dictionary["Password"] = my_password
    with pytest.raises(TypeError):
        sq.systems_status_info(rand_arg=my_string)
