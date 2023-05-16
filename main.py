from startup import create_socket, discover_nodes, ready_for_receiving
from synchronisation import send_multicast


if __name__ == "__main__":
    print("Hello")
    server_instance = create_socket.initialize_server()
    data_storage = discover_nodes.discover_nodes()
    ready_for_receiving.ready_for_receiving_calls()
    
