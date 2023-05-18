import threading

DATA_FILE_LOCK = threading.Lock()
CONFIG_FILE_LOCK = threading.Lock()
SYNC_LOCK = threading.Lock()