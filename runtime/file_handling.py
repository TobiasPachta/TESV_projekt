import json
from synchronisation import mutex

def load_local_data() -> dict:
    try:
        with mutex.SYNC_LOCK:
            with mutex.DATA_FILE_LOCK:
                with open("../TESV_projekt/data/data.json", "r") as infile:
                    return json.load(infile)
    except FileNotFoundError:
        print("No local data file found, create empty file")
        return create_data_file()
    except Exception as e:
        print("Unknown error writing file " + str(e))
    
def save_synced_data(synced_data):
    with mutex.SYNC_LOCK:
        with mutex.DATA_FILE_LOCK:
            with open("../TESV_projekt/data/data.json", "w") as outfile:
                outfile.write(synced_data)

def create_data_file():
    empty_str = "{}"
    try:
        save_synced_data(empty_str)
        return json.load(empty_str)
    except Exception as e:
        print("Writing File failed " + str(e))