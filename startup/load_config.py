import json
import socket

from synchronisation import mutex

def read_config_file():
    try:
        with mutex.CONFIG_FILE_LOCK:
            with open("../TESV_projekt/config/config.json") as json_file:
                config_file = json_file.read()
    except:
        print("Config File missing, shutting down")
        exit()
    return config_file

def load_config_file_to_dict():
    config_as_str = read_config_file()
    config_as_dict = parse_config(config_as_str)
    return config_as_dict

def parse_config(config_as_str):
    return json.loads(config_as_str)

def get_server_config_dict(config_dict):
    return config_dict["server_settings"]

def get_client_config_dict(config_dict):
    return config_dict["client_settings"]

def get_hostmachine_ip_addr():
    own_ip_addr = socket.gethostbyname(socket.gethostname()) 
    return own_ip_addr

def get_server_config():
    server_config_as_dict = get_server_config_dict(load_config_file_to_dict()) 
    return server_config_as_dict

def get_client_config():
    client_config_as_dict = get_client_config_dict(load_config_file_to_dict())
    return client_config_as_dict

def get_multicast_group_from_config(server_settings_dict):
    return server_settings_dict["multicast_group"]

def get_other_nodes_from_config(server_settings_dict):
    other_nodes_list = remove_own_machine_from_node_list(server_settings_dict["node_addresses"])
    return other_nodes_list

def remove_own_machine_from_node_list(node_list):
    host_address = get_hostmachine_ip_addr()
    node_list.remove(host_address)
    return node_list
