import socket
import threading

# List to store connected peer sockets
peer_sockets = []

def handle_peer(peer_socket, peer_address):
    print(f"Connected to peer: {peer_address}")
    try:
        while True:
            message = peer_socket.recv(1024).decode("utf-8")
            if not message:
                break
            print(f"Message from peer {peer_address}: {message}")
    except Exception as e:
        print(f"Error handling message from peer {peer_address}: {e}")
    finally:
        peer_socket.close()
        peer_sockets.remove(peer_socket)

def start_peer(port):
    peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    peer_socket.bind(('0.0.0.0', port))
    peer_socket.listen(5)

    print(f"Peer listening on port {port}")

    while True:
        peer_client_socket, peer_client_address = peer_socket.accept()
        peer_sockets.append(peer_client_socket)
        peer_thread = threading.Thread(target=handle_peer, args=(peer_client_socket, peer_client_address))
        peer_thread.start()

def send_message_to_peer(peer_socket, message):
    try:
        peer_socket.send(message.encode("utf-8"))
    except Exception as e:
        print(f"Error sending message to peer: {e}")

def send_message_to_all(message):
    for peer_socket in peer_sockets:
        send_message_to_peer(peer_socket, message)

if __name__ == "__main__":
    # Start peer
    port = 8000
    peer_thread = threading.Thread(target=start_peer, args=(port,))
    peer_thread.start()

    while True:
        action = input("Enter '1' to connect to a peer and send a message, '2' to send a message to all connected peers, or 'exit' to quit: ")

        if action == 'exit':
            break
        elif action == '1':
            peer_host = input("Enter peer's IP address: ")
            peer_port = int(input("Enter peer's port number: "))
            message = input("Enter message to send: ")
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                client_socket.connect((peer_host, peer_port))
                send_message_to_peer(client_socket, message)
                client_socket.close()
            except Exception as e:
                print(f"Error connecting to peer or sending message: {e}")
        elif action == '2':
            message = input("Enter message to send to all peers: ")
            send_message_to_all(message)
        else:
            print("Invalid action.")
