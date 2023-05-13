from startup import create_socket, discover_nodes


if __name__ == "__main__":
    server_instance = create_socket.initialize_server()
    discover_nodes.discover_nodes()