import socket
import random
import datetime
import json
from time import sleep

from startup import create_socket, load_config


def simple_client():
    print("Welcome!")
    command_description = """
Please choose a command:
[a]dd - to add a new user
[c]hange - to change the status of a user
[g]et - to get the state of a user
[d]elete - to delete the state of a user
[e]xit - to exit the programm
    """
    config_dict = startup()
    config_dict = remove_own_ip_from_config(config_dict)
    sock = open_client_socket(config_dict)
    while True:
        try:
            command = get_input(command_description).lower()
            if sock.fileno() == -1:
                print("Connection lost, restarting")
                sock.close()
                sleep(1)
                sock = open_client_socket(config_dict)
            match command[:1]:
                case "a":
                    add_entry(sock)
                case "c":
                    update_entry(sock)
                case "g":
                    get_entry(sock)
                case "d":
                    delete_entry(sock)
                case "e":
                    print("Goodbye")
                    exit()
                case _:
                    print("Command not known, please try again!")
        except KeyboardInterrupt:
            print("Goodbye")
            exit()


def startup():
    return load_config.get_client_config()

def open_client_socket(config_dict):
    sock = create_socket.create_INET_STREAM_socket()
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    create_socket.bind_socket(sock, load_config.get_hostmachine_ip_addr(), config_dict["client_port"])
    return connect_sock(sock, config_dict)

def connect_sock(sock, config_dict):
    while 1:
        try:
            server_addr = random.choice(config_dict["server_addresses"])
            print("Opening connection " + str(server_addr) + " " + str(config_dict["client_port"]))
            sock.connect((server_addr, config_dict["client_port"]))
            return sock
        except:
            if len(config_dict["server_addresses"]) == 0:
                print("No Servers available!")
                exit()
            config_dict["server_addresses"].remove(server_addr)
            print("Server " + str(server_addr) + " not reached!")

def restart_sock_conn(old_ip, sock):
    config_dict = startup()
    config_dict = remove_own_ip_from_config(config_dict)
    config_dict["server_addresses"].remove(old_ip)
    if len(config_dict["server_addresses"]) > 0:
        sock = open_client_socket(config_dict) 
    else:
        print("no more servers online")
        exit()
    return sock

def remove_own_ip_from_config(config_dict):
    try:
        config_dict["server_addresses"].remove(load_config.get_hostmachine_ip_addr())
    except ValueError:
        pass
    return config_dict
    

def add_entry(sock):
    username  = get_input("Please enter the user you want to add:")
    status = get_input("Please enter the status")
    timestamp = datetime.datetime.now().utcnow()
    dict_for_payload = {"data": [{"username": username, "state": status, "timestamp": str(timestamp)}]}
    payload = str.encode("add" + json.dumps(dict_for_payload))
    send_message_to_server(sock, payload)
    
def update_entry(sock):
    username = get_input("Please enter the user you want to update:")
    status = get_input("Please enter the new status")
    timestamp = datetime.datetime.now().utcnow()
    dict_for_payload = {"data": [{"username": username, "state": status, "timestamp": str(timestamp)}]}
    payload = str.encode("chg" + json.dumps(dict_for_payload))
    send_message_to_server(sock, payload)

def delete_entry(sock):
    username = get_input("Please enter the user you want to delete:")
    dict_for_payload = {"data": [{"username": username}]}
    payload = str.encode("del" + json.dumps(dict_for_payload))
    send_message_to_server(sock, payload)

def get_entry(sock):
    username = get_input("Please enter the user you want to receive:")
    dict_for_payload = {"data": [{"username": username}]}
    payload = str.encode("get" + json.dumps(dict_for_payload))
    send_message_to_server(sock, payload)


def send_message_to_server(sock, payload):
    if sock.fileno() == -1:
        print("Connection lost, restarting")
        old_ip = sock.getpeername()[0]
        sock.close()
        sleep(1)
        sock = restart_sock_conn(old_ip, sock)
        send_message_to_server(sock, payload)
    else:
        sock.sendall(payload)
        response = sock.recv(1024)
        if response.decode() == "":
            print("Connection lost, restarting")
            old_ip = sock.getpeername()[0]
            sock.close()
            sleep(1)
            sock = restart_sock_conn(old_ip, sock)
            send_message_to_server(sock, payload)
        else:
            print(response.decode())

def get_input(message):
    print(message)
    return input(" > ")

if __name__ == '__main__':
    simple_client()
