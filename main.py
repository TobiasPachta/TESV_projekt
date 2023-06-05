from startup import create_socket, discover_nodes, ready_for_receiving
from synchronisation import send_multicast, synch_nodes
from runtime import message_handling

import os
import json

def simple_server():
    create_socket.initialize_server()
    discover_nodes.discover_nodes()
    ready_for_receiving.ready_for_receiving_calls()


if __name__ == "__main__":
    simple_server()