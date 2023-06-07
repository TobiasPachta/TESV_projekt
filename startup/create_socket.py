import socket
import struct

from startup import load_config

def initialize_server():
    server_settings_dict = load_config.get_server_config()
    server_sock = create_server(server_settings_dict)
    return server_sock

def create_server(settings_dict):
    host_address = load_config.get_hostmachine_ip_addr()
    if not host_address in settings_dict["node_addresses"]:
        print("Machine not registered as node, please check the configuration: " + host_address)
        exit()
    server_instance = create_INET_STREAM_socket()
    bind_socket(server_instance, host_address, settings_dict["client_port"])
    return server_instance

def create_INET_STREAM_socket():
    tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    return tcp_sock

def create_multicast_socket():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ttl = struct.pack('b', 1)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)
    return sock

def bind_socket(socket, ip_addr, port):
    socket.bind((ip_addr, port))