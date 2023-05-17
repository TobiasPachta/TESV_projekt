import socket
import struct
import threading
import json

from startup import load_config,create_socket
from synchronisation import send_multicast

def ready_for_receiving_calls():
    server_config = load_config.get_server_config()
    open_mc_sync_socket(server_config)
    open_transmission_socket(server_config)

def open_mc_sync_socket(server_config):
    message, multicast_group = send_multicast.set_multicast_config(server_config)
    sock = create_socket.create_multicast_socket()
    sock.bind(multicast_group)
    group = socket.inet_aton(server_config["multicast_group"])
    mreq = struct.pack("4sI", group, socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #if there are address conflicts, don't think we need it
    t = threading.Thread(target=handle_mc_sync_req, args=(sock,))
    t.start()


def open_transmission_socket(server_config):
    sock = create_socket.create_INET_STREAM_socket()
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    create_socket.bind_socket(sock, load_config.get_hostmachine_ip_addr(), server_config["sync_port"])
    sock.listen(3)
    while True:
        conn, addr = sock.accept()
        print("Incoming connection on %s" % sock.getsockname())
        t = threading.Thread(target=handle_sync_response, args=(conn,addr))
        t.start()

def handle_mc_sync_req(sock):
    while True:
        message, sender = receive_and_decode_message(sock)
        if message == "sync_req":
            sock.sendto("ack".encode(), sender)

def handle_sync_response(connection, address):
    message, sender = receive_and_decode_message(connection)
    if message == "sync_req":
        data = send_multicast.load_local_data()
        print(str(data))
        print(type(data))
        transmission_data = str.encode(json.dumps(data))
        connection.sendall(transmission_data)


def receive_and_decode_message(connection):
    message, sender = connection.recvfrom(1024)
    return message.decode(), sender