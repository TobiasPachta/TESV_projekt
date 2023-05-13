import socket

from startup import load_config

def initialize_server():
    config_dict = load_config.load_config_file_to_dict()
    server_settings_dict = load_config.get_server_config(config_dict)
    return create_server(server_settings_dict)

def create_server(settings_dict):
    host_address = load_config.get_hostmachine_ip_addr()
    if not host_address in settings_dict["node_addresses"]:
        print("Machine not registered as node, please check the configuration: " + host_address)
        exit()
    server_instance = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_instance.bind((host_address, settings_dict["client_port"]))
    return server_instance
