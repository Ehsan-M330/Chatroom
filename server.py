import socket
import threading

# Dictionary to store client connections and their nicknames
clients = {}

# Function to handle client connections
def handle_client(client_socket, client_address):
    print(f"[NEW CONNECTION] {client_address} connected.")

    # Requesting client's nickname
    client_socket.send("Enter your nickname: ".encode())
    nickname = client_socket.recv(1024).decode()
    clients[client_socket] = nickname

    if (nickname!="listener"):
        # Informing other clients about the new connection
        broadcast(f"{nickname} has joined the chat!")
        # Set timeout for 60 seconds
        client_socket.settimeout(60)

        try:
            while True:
                message = client_socket.recv(1024).decode()
                if message:
                    if message.lower() == "exit":
                        break
                    broadcast(f"{nickname}: {message}")
                    # Reset the timeout for inactivity
                    client_socket.settimeout(60)
        except:
            pass
        
        broadcast(f"{nickname} has left the chat.")  
              
    else:
        try:
            while True:
                message = client_socket.recv(1024).decode()
                if message:
                        if message.lower() == "exit":
                            break
        except:
            pass           
    # Closing the connection
    del clients[client_socket]
    client_socket.close()
    
# Function to broadcast messages to all clients
def broadcast(message):
    for client_socket in clients:
        try:
            client_socket.send(message.encode())
        except:
            pass

# Main function
def main():
    host = "127.0.0.1"
    port = 12345

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen()

    print(f"[SERVER STARTED] Listening on {host}:{port}...")

    try:
        while True:
            client_socket, client_address = server_socket.accept()
            client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
            client_thread.start()
            
            
    except KeyboardInterrupt:
        print("[SERVER STOPPED]")

    server_socket.close()

if __name__ == "__main__":
    main()
