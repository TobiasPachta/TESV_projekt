import json

from synchronisation import mutex, send_multicast
from startup import load_config, create_socket
from runtime import clock, file_handling

def send_new_data_to_nodes(new_data):
    with mutex.SYNC_LOCK:
        server_config = load_config.get_server_config()
        message, multicast_group = send_multicast.set_multicast_config(server_config)
        new_data["counter"] = clock.EVENT_COUNTER
        message = "new_data" + json.dumps(new_data)
        mc_sock = create_socket.create_multicast_socket()
        try:
            mc_sock.sendto(message.encode(), multicast_group)
        finally:
            mc_sock.close()
