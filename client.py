import socket
import threading

# Function to receive messages from the server
def receive_messages(client_socket):
    try:
        while True:
            message = client_socket.recv(1024).decode()
            print(message)
    except:
        pass

# Main function
def main():
    host = "127.0.0.1"
    port = 12345

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()

    try:
        while True:
            message = input()
            if message.lower() == "exit":
                break
            client_socket.send(message.encode())
    except KeyboardInterrupt:
        pass

    client_socket.close()

if __name__ == "__main__":
    main()
