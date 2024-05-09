import socket
import threading

clients = {}
timeout=60

def handle_client(client_socket, client_address):
    print(f"[NEW CONNECTION] {client_address} connected.")

    client_socket.send("Enter your nickname: ".encode())
    nickname = client_socket.recv(1024).decode()
    clients[client_socket] = nickname

    if (nickname!="listener"):

        broadcast(f"{nickname} has joined the chat!")

        client_socket.settimeout(timeout)

        try:
            while True:
                message = client_socket.recv(1024).decode()
                if message:
                    if message.lower() == "exit":
                        break
                    broadcast(f"{nickname}: {message}")
            
                    client_socket.settimeout(timeout)
        except:
            pass
        
        del clients[client_socket]
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
                   
        del clients[client_socket]
    
    client_socket.close()
    print(f"[CONNECTION] {client_address} disconnected.")
    
def broadcast(message):
    for client_socket in clients:
        try:
            client_socket.send(message.encode())
        except:
            pass

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
    except:
        pass
    

if __name__ == "__main__":
    main()
