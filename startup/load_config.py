import json
import socket

def read_config_file():
    try:
        with open("config/config.json") as json_file:
            config_file = json_file.read()
    except:
        print("Config File missing, shutting down")
        exit()
    return config_file

def load_config_file_to_dict():
    config_as_str = read_config_file()
    return parse_config(config_as_str)

def parse_config(config_as_str):
    return json.loads(config_as_str)

def get_server_config(config_dict):
    return config_dict["server_settings"]

def get_hostmachine_ip_addr():
    return socket.gethostbyname(socket.gethostname())