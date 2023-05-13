import socket
import struct

def startup_discover_multicast(mc_group):
    message = 'synchronisation request'
    multicast_group = (mc_group, 23456)
    sock = set_up_socket_with_options()
    try:
        sock.sendto(message.encode(), multicast_group)
        replied_server_list = wait_for_mc_response(sock)
    finally:
        sock.close()
    if(replied_server_list.count == 0):
        print("no response from other nodes")
        #first server online, read local data 

def set_up_socket_with_options():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(0.2)
    ttl = struct.pack('b', 1)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)
    return sock

def wait_for_mc_response(sock) -> list:
    replied_server_list = []
    while True:
        try:
            data, server = sock.recvfrom(16)
        except socket.timeout:
            print("Timeout")
            break
        else:
            print("received answer %s from %s", data, server)
            replied_server_list.append(server)
    return replied_server_list
    