
from startup import load_config, create_socket
from synchronisation import send_multicast, synch_nodes

def discover_nodes():
    config_dict = load_config.load_config_file_to_dict()
    server_settings_dict = load_config.get_server_config(config_dict)
    other_nodes_list = get_other_nodes_from_config(server_settings_dict)
    multicast_group = get_multicast_group_from_config(server_settings_dict)
    return send_multicast.startup_discover_multicast(multicast_group, other_nodes_list)


def get_other_nodes_from_config(server_settings_dict):
    return remove_own_machine_from_node_list(server_settings_dict["node_addresses"])

def remove_own_machine_from_node_list(node_list):
    host_address = load_config.get_hostmachine_ip_addr()
    node_list.remove(host_address)

def get_multicast_group_from_config(server_settings_dict):
    return server_settings_dict["multicast_group"]