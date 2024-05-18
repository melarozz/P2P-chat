import socket
import threading

def handle_peer(peer_socket, peer_address):
    print(f"Connected to peer: {peer_address}")
    while True:
        try:
            message = peer_socket.recv(1024).decode("utf-8")
            if message:
                print(f"Message from peer {peer_address}: {message}")
        except:
            print(f"Error handling message from peer {peer_address}")
            break

def start_peer(port):
    peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    peer_socket.bind(('0.0.0.0', port))
    peer_socket.listen(5)

    print(f"Peer listening on port {port}")

    while True:
        peer_client_socket, peer_client_address = peer_socket.accept()
        peer_thread = threading.Thread(target=handle_peer, args=(peer_client_socket, peer_client_address))
        peer_thread.start()

def send_message_to_peer(peer_host, peer_port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((peer_host, peer_port))
        while True:
            message = input("Enter message to send (or type 'disconnect' to connect to another peer): ")
            if message.lower() == 'disconnect':
                break

            client_socket.send(message.encode("utf-8"))
    except Exception as e:
        print(f"Error sending message to peer {peer_host}:{peer_port}: {e}")
    finally:
        client_socket.close()

if __name__ == "__main__":
    # Start peer
    port = 8000
    peer_thread = threading.Thread(target=start_peer, args=(port,))
    peer_thread.start()

    while True:
        # Connect to another peer
        peer_host = input("Enter peer's IP address (or type 'exit' to quit): ")
        if peer_host.lower() == 'exit':
            break

        peer_port = int(input("Enter peer's port number: "))

        # Start sending messages
        send_thread = threading.Thread(target=send_message_to_peer, args=(peer_host, peer_port))
        send_thread.start()
