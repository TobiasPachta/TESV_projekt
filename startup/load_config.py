import json

def read_config_file():
    try:
        with open("config/config.json") as json_file:
            config_file = json_file.read()
    except:
        print("Config File missing, shutting down")
        exit()
    return config_file

def parse_config(config_as_str):
    return json.loads(config_as_str)
