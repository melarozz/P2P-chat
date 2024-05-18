import socket
import threading

def handle_connection(conn, addr):
    print(f"Connected to {addr}")

    while True:
        try:
            data = conn.recv(1024).decode("utf-8")
            if data:
                print(f"Message from {addr}: {data}")
                broadcast(data, conn)
            else:
                print(f"{addr} disconnected")
                remove_connection(conn)
                break
        except:
            print(f"Error handling message from {addr}")
            remove_connection(conn)
            break

def broadcast(message, sender):
    for connection in connections:
        if connection != sender:
            try:
                connection.send(message.encode("utf-8"))
            except:
                print("Error broadcasting message")

def remove_connection(conn):
    if conn in connections:
        connections.remove(conn)

def start_peer():
    global connections
    connections = []

    host = 'localhost'
    port = 9999

    peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    peer_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    peer_socket.bind((host, port))
    peer_socket.listen(5)

    print("Peer-to-peer chat started.")

    while True:
        conn, addr = peer_socket.accept()
        connections.append(conn)

        conn_thread = threading.Thread(target=handle_connection, args=(conn, addr))
        conn_thread.start()

        # Connect to other peers
        for other_addr in peer_addresses:
            if other_addr != addr:  # Avoid connecting to self
                try:
                    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    client_socket.connect(other_addr)
                    connections.append(client_socket)
                    client_thread = threading.Thread(target=handle_connection, args=(client_socket, other_addr))
                    client_thread.start()
                except Exception as e:
                    print(f"Error connecting to {other_addr}: {e}")

# List of other peer addresses
peer_addresses = [('localhost', 9998), ('localhost', 9997)]  # Add more peers as needed

start_peer()
