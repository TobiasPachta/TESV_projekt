import socket
import json

from startup import create_socket, discover_nodes, load_config, ready_for_receiving

def test_create_socket_initialize_server_class():
    sock = create_socket.initialize_server()
    assert str(type(sock)) == "<class 'socket.socket'>"

def test_create_socket_initialize_server_address():
    sock = create_socket.initialize_server()
    print(sock.getsockname())
    assert str(sock.getsockname()) == "('" + str(socket.gethostbyname(socket.gethostname())) + "', 12345)" 

def test_create_socket_create_INET_STREAM_socket_type():
    sock = create_socket.create_INET_STREAM_socket()
    assert sock.type == socket.SocketKind.SOCK_STREAM 

def test_create_socket_create_INET_STREAM_socket_family():
    sock = create_socket.create_INET_STREAM_socket()
    assert sock.family == socket.AddressFamily.AF_INET 

def test_create_socket_create_multicast_socket_type():
    sock = create_socket.create_multicast_socket()
    assert sock.type == socket.SocketKind.SOCK_DGRAM 

def test_create_socket_create_multicast_socket_family():
    sock = create_socket.create_multicast_socket()
    assert sock.family == socket.AddressFamily.AF_INET 

def test_create_socket_create_multicast_socket_ttl():
    sock = create_socket.create_multicast_socket()
    assert sock.getsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL) == 1

def test_create_socket_bind_socket():
    sock = create_socket.create_INET_STREAM_socket()
    create_socket.bind_socket(sock, "0.0.0.0", 11111)
    assert str(sock.getsockname()) == "('0.0.0.0', 11111)"

def test_discover_nodes():
    data = discover_nodes.discover_nodes()
    assert str(data) == "{'username': 'Tobias'}"

def test_load_config_read_config_file_nempty():
    config_file = load_config.read_config_file()
    assert config_file != ""

def test_load_config_load_config_file_to_dict():
    config_as_dict = load_config.load_config_file_to_dict()
    assert str(type(config_as_dict)) == "<class 'dict'>"

def test_load_config_parse_config():
    config_as_str = load_config.read_config_file()
    config_as_dict = load_config.parse_config(config_as_str)
    assert config_as_dict == json.loads(config_as_str)

def test_load_config_get_server_config_dict_nempty():
    config_as_dict = load_config.load_config_file_to_dict()
    server_settings_dict = load_config.get_server_config_dict(config_as_dict)
    assert server_settings_dict != ""

def test_load_config_get_hostmachine_ip_addr():
    assert load_config.get_hostmachine_ip_addr() == socket.gethostbyname(socket.gethostname())

def test_load_config_get_server_config_nempty():
    assert str(load_config.get_server_config()) != ""

    
def test_load_config_get_server_config_nempty():
    assert str(type(load_config.get_server_config())) == "<class 'dict'>"

def test_load_config_get_multicast_group_from_config_nempty():
    server_settings = load_config.get_server_config()
    mc_group = load_config.get_multicast_group_from_config(server_settings)
    assert mc_group != ""

def test_load_config_get_other_nodes_from_config_nempty():
    server_settings = load_config.get_server_config()
    other_nodes = load_config.get_other_nodes_from_config(server_settings)
    assert other_nodes != ""

def test_load_config_remove_own_machine_from_node_list():
    server_settings = load_config.get_server_config()
    all_nodes = server_settings["node_addresses"]
    other_nodes = load_config.remove_own_machine_from_node_list(all_nodes)
    own_ip = load_config.get_hostmachine_ip_addr()
    assert not own_ip in other_nodes
