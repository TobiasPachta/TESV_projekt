from startup import create_socket, discover_nodes
from synchronisation import send_multicast


if __name__ == "__main__":
    server_instance = create_socket.initialize_server()
    data_storage = discover_nodes.discover_nodes()
    print(data_storage)
