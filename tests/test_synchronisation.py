import socket
import json

from synchronisation import send_multicast, synch_nodes
from startup import load_config

def test_send_multicast_startup_discover_multicast():
    return_val = send_multicast.startup_discover_multicast()
    assert str(type(return_val)) == "<class 'dict'>"

def test_send_multicast_validate_received_data_true():
    data_valid = send_multicast.validate_received_data('{"username": "Tobias"}')
    assert data_valid == True

def test_send_multicast_validate_received_data_false():
    data_valid = send_multicast.validate_received_data("not a json")
    assert data_valid == False

def test_send_multicast_validate_responder_true():
    valid_responder = send_multicast.validate_responder("192.168.0.2", ["192.168.0.1", "192.168.0.2", "192.168.0.3"])
    assert valid_responder == True

    
def test_send_multicast_validate_responder_false():
    valid_responder = send_multicast.validate_responder("192.168.0.100", ["192.168.0.1", "192.168.0.2", "192.168.0.3"])
    assert valid_responder == False

def test_send_multicast_set_multicast_config_msg():
    server_config = load_config.get_server_config()
    message, mc_group = send_multicast.set_multicast_config(server_config)
    assert message == "sync_req"

def test_send_multicast_set_multicast_config_mc_grp():
    server_config = load_config.get_server_config()
    message, mc_group = send_multicast.set_multicast_config(server_config)
    assert str(mc_group) == "('224.18.0.1', 23456)"