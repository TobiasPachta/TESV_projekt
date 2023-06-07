import socket
import struct
import json

from startup import create_socket, load_config
from runtime import file_handling
from runtime import clock

def startup_discover_multicast():
    server_config = load_config.get_server_config()
    message, multicast_group = set_multicast_config(server_config)
    other_nodes_list = load_config.get_other_nodes_from_config(server_config)
    mc_sock = create_socket.create_multicast_socket()
    mc_sock.settimeout(0.2)
    try:
        mc_sock.sendto(message.encode(), multicast_group)
        replied_server_list = wait_for_mc_response(mc_sock)
    finally:
        mc_sock.close()
    if(len(replied_server_list) == 0):
        print("no response from other nodes")
        synced_data = file_handling.load_local_data()
        return synced_data
    replied_server_list.sort()
    counter = 0
    sock = create_socket.create_INET_STREAM_socket()
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    create_socket.bind_socket(sock, load_config.get_hostmachine_ip_addr(), server_config["sync_port"])
    while True:
        try:
            if (validate_responder(replied_server_list[counter], other_nodes_list)):
                #print("node %s trusted, connecting" % replied_server_list[counter])
                sock.connect((replied_server_list[counter], server_config["sync_port"]))
                sock.send(("sync_req").encode())
                synced_data = receive_sync_data(sock)
                if validate_received_data(synced_data):
                    try_save_synced_data_to_disk(synced_data)
                    print("Synchronisation successful!")
                    break
                else:
                    print("Received data is not a valid JSON structure")
                    counter += 1
                    continue
            else:
                print("Responder %s not trusted" % replied_server_list[counter])
                counter += 1
                continue
        except IndexError:
            print("No Data received, no node responded")
            synced_data = file_handling.load_local_data()
            break
        except Exception as e:
            print(str(e))
            print("Node %s not reached" % replied_server_list[counter])
            counter += 1
            continue
    sock.close()
    return synced_data

def receive_sync_data(sock):
    data = sock.recv(1024)
    return data.decode()

def validate_received_data(data):
    try:
        json.loads(data)
        return True
    except Exception as e:
        print("data incorrect" + str(e))
        return False

def wait_for_mc_response(sock) -> list:
    replied_server_list = []
    while True:
        try:
            #we only want the ip address, the data is not relevant and the port will change anyway (mc->sc)
            data, (server, port) = sock.recvfrom(16)
        except socket.timeout:
            break
        else:
            replied_server_list.append(server)
    return replied_server_list


def validate_responder(responder_ip_addr, other_nodes_list):
    return True if responder_ip_addr in other_nodes_list else False
    
def try_save_synced_data_to_disk(synced_data):
    try:
        data_as_dict = json.loads(synced_data)
        clock.set_event_counter(data_as_dict["counter"])
        data_as_dict.pop("counter")
        file_handling.save_synced_data(json.dumps(data_as_dict))
    except Exception as e:
        print("Writing File failed " + str(e))
        exit()

def set_multicast_config(server_config):
    message = "sync_req"
    mc_group = load_config.get_multicast_group_from_config(server_config)
    multicast_group = (mc_group, server_config["mc_port"])
    return message, multicast_group