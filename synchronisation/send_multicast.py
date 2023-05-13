import socket
import struct
import json

from startup import create_socket, load_config

def startup_discover_multicast(mc_group):
    server_config = get_server_config()
    message = 'synchronisation request'
    multicast_group = (mc_group, 23456)
    sock = create_multicast_socket()
    try:
        sock.sendto(message.encode(), multicast_group)
        replied_server_list = wait_for_mc_response(sock)
    finally:
        sock.close()
    if(len(replied_server_list) == 0):
        print("no response from other nodes")
        #first server online, read local data 
    else:
        replied_server_list.sort()
        counter = 0
        sock = create_socket.create_INET_STREAM_socket()
        create_socket.bind_socket(sock, load_config.get_hostmachine_ip_addr(), server_config["sync_port"])
        while True:
            try:
                sock.connect((replied_server_list[counter], server_config["sync_port"]))
                sock.send(("sync_req").encode())
                synced_data = receive_sync_data(sock)
                if validate_received_data(synced_data):
                    
                    break
                else:
                    continue
            except IndexError:
                print("No Data received, no node responded")
                break
            except:
                print("Node %s not reached", replied_server_list[counter])
        sock.close()

def receive_sync_data(sock):
    data = sock.recv(1024)
    return data.decode()

def validate_received_data(data):
    try:
        json.load(data)
        return True
    except:
        print("Received data invalid")
        return False

def create_multicast_socket():
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
    
def get_server_config():
    return load_config.get_server_config(load_config.load_config_file_to_dict())