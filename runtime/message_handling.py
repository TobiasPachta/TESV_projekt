import socket
import json

from synchronisation import mutex, synch_nodes
from runtime import file_handling, clock


def receive_and_decode_message(connection):
    message, sender = connection.recvfrom(1024)
    return message.decode(), sender

def add_or_update_entry(message):
    updated = False
    local_data = file_handling.load_local_data()
    message_as_dict, message_as_list = get_message_as_dict_and_list(message)
    for entry in local_data["data"]:
        if entry["username"] == message_as_list["username"]:
            entry["state"] = message_as_list["state"]
            entry["timestamp"] = message_as_list["timestamp"]
            updated = True
            break
    if updated:
        file_handling.save_synced_data(json.dumps(local_data))
    else:
        appended_list = add_entry(local_data, message_as_dict["data"][0])
        #appended_list.pop("counter")
        file_handling.save_synced_data(json.dumps(appended_list))
    clock.set_event_counter(str(clock.EVENT_COUNTER + 1))
    synch_nodes.send_new_data_to_nodes(local_data)
    return updated
    

def delete_entry(message):
    updated = False
    local_data = file_handling.load_local_data()
    message_as_dict, message_as_list = get_message_as_dict_and_list(message)
    for entry in local_data["data"]:
        if entry["username"] == message_as_list["username"]:
            local_data["data"].remove(entry)
            file_handling.save_synced_data(json.dumps(local_data))
            updated = True
            break
    clock.set_event_counter(str(clock.EVENT_COUNTER + 1))
    synch_nodes.send_new_data_to_nodes(local_data)
    return updated

def send_entry(message):
    local_data = file_handling.load_local_data()
    print(str(type(local_data)))
    message_as_dict, message_as_list = get_message_as_dict_and_list(message)
    for entry in local_data["data"]:
        if entry["username"] == message_as_list["username"]:
            return entry
    return "No entry with username " + message_as_list["username"] + " found"


def add_entry(local_data: dict, entry_to_add):
    local_data["data"].append(entry_to_add)
    return local_data


def get_message_as_dict_and_list(message_as_str):
    message_as_dict = json.loads(message_as_str)
    return message_as_dict, message_as_dict["data"][0]

def save_synced_data(message):
    message_as_dict = json.loads(message)
    if int(message_as_dict["counter"]) > clock.EVENT_COUNTER:
        new_counter = message_as_dict["counter"]
        message_as_dict.pop("counter")
        file_handling.save_synced_data(json.dumps(message_as_dict))
        clock.set_event_counter(new_counter)