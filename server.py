import socket
import threading
import signal
import sys

# Dictionary created to store client username
client_username = {}

# Function to handle incoming client connections
def handle_client(client_socket, client_address):
    print(f"Connection from {client_address}")

    # Prompt Client for their username
    client_socket.send("Enter your username:".encode("utf-8"))
    username = client_socket.recv(1024).decode("utf-8")

    # Store the client's username
    client_username[client_socket] = username

    while True:
        # Receive message from client
        message = client_socket.recv(1024).decode("utf-8")
        if not message:
            break
        print(f"Received from {username}:{message}")

        # Broadcast message to all clients except the sender
        broadcast(f"{username}:{message}", client_socket)

    # Remove client from dictionary when  they disconnect
    del client_username[client_socket]

    # Close client connection
    client_socket.close()
    print(f"Connection from {client_address} closed")

# Function to broadcast message to all connected clients except the sender
def broadcast(message, sender_socket):
    with clients_lock:
        for client in clients[:]:
            if client != sender_socket:
                try:
                    client.send(message.encode("utf-8"))
                except BrokenPipeError:
                    print("Broken pipe: Client disconnected.")
                    clients.remove(client)
                except Exception as e:
                    print(f"An error occurred while sending message: {e}")

# Function to gracefully shutdown the server
def shutdown_server(signal, frame):
    print("Server shutting down...")
    # Close all client connections
    for client_socket in clients:
        client_socket.close()
    # Close the server socket
    server_socket.close()
    sys.exit(0)

# Server configuration
HOST = '127.0.0.1'  # Localhost
PORT = 8080

# Create socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)

print(f"Server listening on {HOST}:{PORT}")

clients = []
clients_lock = threading.Lock()  # Lock for synchronizing access to clients list

# Register signal handler for graceful shutdown
signal.signal(signal.SIGINT, shutdown_server)

# Accept incoming connections and start a new thread for each client
while True:
    try:
        client_socket, client_address = server_socket.accept()
        with clients_lock:
            clients.append(client_socket)
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()
    except KeyboardInterrupt:
        print("Server shutting down...")
        break
    except Exception as e:
        print(f"An error occurred while accepting connections: {e}")
        breakimport socket