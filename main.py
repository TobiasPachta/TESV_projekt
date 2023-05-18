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
    print("Hello")
    #new_dict_message = '{"data": [{"username": "Tobias", "state": "das", "timestamp": "2022-01-03T13:30:00+01:00"}], "counter": "1"}'
    #message_handling.add_or_update_entry(new_dict_message)
    #message_to_delete = '{"data": [{"username":"A"}]}'
    #print(message_handling.delete_entry(message_to_delete))
    #message_to_send = '{"data": [{"username":"a"}]}'
    #print(message_handling.send_entry(message_to_send))
    #print(synch_nodes.send_new_data_to_nodes(json.loads(new_dict_message)))
    #message_handling.save_synced_data(new_dict_message)
    simple_server()