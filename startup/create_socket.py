import socket

from startup import load_config

def initialize_server():
    config_dict = load_config.parse_config(load_config.read_config_file())
    server_settings_dict = config_dict["server_settings"]
    return create_server(server_settings_dict)


def create_server(settings_dict):
    host_address = socket.gethostbyname(socket.gethostname())
    server_instance = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #server_instance.bind((host_address, settings_dict["port_number"]))
    server_instance.bind(("", settings_dict["port_number"]))
    return server_instance
