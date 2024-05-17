import socket
import threading

# Client configuration
HOST = '127.0.0.1'  # Localhost
PORT = 8080

# Connect to server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))


# Function to prompt the user for their username
def get_username():
    username = input("Enter your username:")
    client_socket.send(username.encode("utf-8"))

# Display Welcome Message
print("Welcome to Group F Chat Application")

# Function to receive messages from server
def receive_messages():
    while True:
        try:
            message = client_socket.recv(1024).decode("utf-8")
            if not message:
                print("Server disconnected.")
                break
            print(message)
        except ConnectionResetError:
            print("Server reset the connection.")
            break
        except ConnectionAbortedError:
            print("Server aborted the connection.")
            break
        except Exception as e:
            print(f"An error occurred: {e}")
            break

# Function to send messages to the server
def send_message():
    while True:
        message = input(" ") # Prompt the user to input a message
        print(f"You: {message}")
        client_socket.send(message.encode("utf-8")) # send the message to the server


# Start thread to receive messages
receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

# Start thread to send messages
send_thread = threading.Thread(target=send_message)
send_thread.start()