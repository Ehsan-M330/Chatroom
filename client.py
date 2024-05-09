import socket
import threading

def receive_messages(client_socket):
    
    while True:
        try:
                message = client_socket.recv(1024).decode()
                if message=='':
                    break
                print(message)
                
        except:
            break
    print("You have left the chat.") 
    client_socket.close()
    
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
    except:
        pass
    
    client_socket.close()

if __name__ == "__main__":
    main()
