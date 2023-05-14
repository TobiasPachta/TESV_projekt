import socket
import struct
import json

from startup import create_socket, load_config

def startup_discover_multicast(mc_group, other_nodes_list):
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
        synced_data = load_local_data()
    else:
        replied_server_list.sort()
        counter = 0
        sock = create_socket.create_INET_STREAM_socket()
        create_socket.bind_socket(sock, load_config.get_hostmachine_ip_addr(), server_config["sync_port"])
        while True:
            try:
                if (validate_responder(replied_server_list[counter], other_nodes_list)):
                    sock.connect((replied_server_list[counter], server_config["sync_port"]))
                    sock.send(("sync_req").encode())
                    synced_data = receive_sync_data(sock)
                    if validate_received_data(synced_data):
                        try:
                            save_synced_data(synced_data)
                            print("Saved synced data to disk")
                            break
                        except:
                            print("Writing File failed " + Exception)
                            exit()
                    else:
                        print("Received data is not a valid JSON structure")
                        counter += 1
                        continue
                else:
                    print("Responder %s not trusted", replied_server_list[counter])
                    counter += 1
                    continue
            except IndexError:
                print("No Data received, no node responded")
                synced_data = load_local_data()
                break
            except:
                print("Node %s not reached", replied_server_list[counter])
                counter += 1
                continue
        sock.close()
    return synced_data

def receive_sync_data(sock):
    data = sock.recv(1024)
    return data.decode()

def validate_received_data(data):
    try:
        json.load(data)
        return True
    except:
        return False

def save_synced_data(synced_data):
    with open("data/data.json", "w") as outfile:
        outfile.write(synced_data)

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
            break
        else:
            print("received answer %s from %s", data, server)
            replied_server_list.append(server)
    return replied_server_list
    
def get_server_config():
    return load_config.get_server_config(load_config.load_config_file_to_dict())

def load_local_data():
    try:
        with open("data/data.json", "r") as infile:
            return json.load(infile)
    except FileNotFoundError:
        print("No local data file found, create empty file")
        return create_data_file()

def create_data_file():
    empty_str = "{}"
    try:
        save_synced_data(empty_str)
        return load_local_data()
    except Exception as e:
        print("Writing File failed " + str(e))

def validate_responder(responder_ip_addr, other_nodes_list):
    return True if responder_ip_addr in other_nodes_list else False
    