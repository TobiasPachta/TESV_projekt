import socket
import struct
import threading
import json

from startup import load_config,create_socket
from synchronisation import send_multicast
from runtime import connection_handling, message_handling

def ready_for_receiving_calls():
    all_threads = []
    server_config = load_config.get_server_config()
    all_threads.append(open_mc_sync_socket(server_config))
    t = threading.Thread(target=open_transmission_socket, args=(server_config,))
    t.start()
    all_threads.append(t)
    open_data_socket(server_config, all_threads)

def open_mc_sync_socket(server_config):
    message, multicast_group = send_multicast.set_multicast_config(server_config)
    sock = create_socket.create_multicast_socket()
    sock.bind(multicast_group)
    group = socket.inet_aton(server_config["multicast_group"])
    mreq = struct.pack("4sI", group, socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.settimeout(0.5)
    print("Listening for MC on " + str(multicast_group))
    t = threading.Thread(target=connection_handling.handle_mc_sync_req, args=(sock,))
    t.start()
    return t


def open_transmission_socket(server_config):
    mainThread = threading.currentThread()
    sock = create_socket.create_INET_STREAM_socket()
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    create_socket.bind_socket(sock, load_config.get_hostmachine_ip_addr(), server_config["sync_port"])
    sock.settimeout(0.5)
    print("Listening for syn on " + str(sock.getsockname()))
    sock.listen(3)
    threadList = []
    try:
        while getattr(mainThread, "shouldStop", True):
            try:
                conn, addr = sock.accept()
                print("Incoming connection from %s:%s" % (addr))
                t = threading.Thread(target=connection_handling.handle_sync_response, args=(conn,addr))
                t.start()
                threadList.append(t)
            except socket.timeout:
                pass
        print("Shutting down transmission server")
    except KeyboardInterrupt:
        print("Shutting down transmission server")
    finally:
        if sock:
            sock.close()
        for t in threadList:
            t.shouldStop = False
            t.join()


def open_data_socket(server_config, allThreads):
    sock = create_socket.create_INET_STREAM_socket()
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    create_socket.bind_socket(sock, load_config.get_hostmachine_ip_addr(), server_config["client_port"])
    sock.settimeout(0.5)
    print("Listening for clients on " + str(sock.getsockname()))
    sock.listen(3)
    try:
        while True:
            try:
                conn, addr = sock.accept()
                print("Incoming client transmission from %s:%s" % (addr))
                t = threading.Thread(target=connection_handling.handle_client_request, args=(conn, addr))
                t.start()
                allThreads.append(t)
            except socket.timeout:
                pass
    except KeyboardInterrupt:
        print("Shutting down data server")
    finally:
        if sock:
            sock.close()
        print(allThreads)
        for t in allThreads:
            t.shouldStop = False
            t.join()
