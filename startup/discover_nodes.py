
from startup import load_config, create_socket
from synchronisation import send_multicast, synch_nodes

def discover_nodes():
    return send_multicast.startup_discover_multicast()
