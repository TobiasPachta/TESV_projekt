import json
import socket
import threading

from runtime import message_handling,file_handling, clock
from synchronisation import send_multicast, mutex


def handle_client_request(connection, address):
    t = threading.currentThread()
    connection.settimeout(5.0)
    print("Socket opened at %s:%s" % (address))
    while getattr(t, "shouldStop", True):
        try:
            message = connection.recv(1024)
            message = message.decode()
            match message[:3]:
                case "add":
                    updated = message_handling.add_or_update_entry(message[3:])
                    if updated:
                        connection.sendall("Status has been updated!".encode())
                    else:
                        connection.sendall("New user had been created!".encode())
                case "del":
                    updated = message_handling.delete_entry(message[3:])
                    if updated:
                        connection.sendall("Entry has been deleted!".encode())
                    else:
                        connection.sendall("No entry with provided username was found!".encode())
                case "chg":
                    updated = message_handling.add_or_update_entry(message[3:])
                    if updated:
                        connection.sendall("Status has been updated!".encode())
                    else:
                        connection.sendall("New user had been created!".encode())
                case "get":
                    entry = message_handling.send_entry(message[3:])
                    connection.sendall(str(entry).encode())
                case _:
                    print("unknown request %s" % (message[:3]))
                    break
        except socket.timeout:
            pass
    print("Socket at %s:%s closed" % (address))
    connection.shutdown(socket.SHUT_WR)
    connection.close()
        

def handle_mc_sync_req(sock):
    t = threading.currentThread()
    try:
        while getattr(t, "shouldStop", True):
            try:
                message, sender = message_handling.receive_and_decode_message(sock)
                print("Incoming mc-connection from %s:%s" % (sender))
                if sender[0] != sock.getsockname()[0]:
                    match message[:8]:
                        case "sync_req":
                            sock.sendto("ack".encode(), sender)
                        case "new_data":
                            message_handling.save_synced_data(message[8:])
                        case _:
                            #ignore message
                            pass
            except socket.timeout:
                pass
        print("Shutting down mc server")
    except KeyboardInterrupt:
        print("Shutting down mc server")
    finally:
        if sock:
            sock.close()
        

def handle_sync_response(connection, address):
    message, sender = message_handling.receive_and_decode_message(connection)
    if message == "sync_req":
        send_data_to_node(connection)

def send_data_to_node(connection):
    data = file_handling.load_local_data()
    data["counter"] = clock.EVENT_COUNTER
    transmission_data = str.encode(json.dumps(data))
    connection.sendall(transmission_data)
    connection.close()
    

