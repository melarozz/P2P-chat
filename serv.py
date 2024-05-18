import socket
import threading

def receive_messages(sock):
    while True:
        message = sock.recv(1024).decode("utf-8")
        print(message)

def send_message(sock):
    while True:
        message = input()
        sock.send(message.encode("utf-8"))

def start_chat(host, port):
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.bind((host, port))
    server_sock.listen(1)
    print(f"Listening on {host}:{port}")

    while True:
        client_sock, _ = server_sock.accept()
        threading.Thread(target=receive_messages, args=(client_sock,)).start()
        threading.Thread(target=send_message, args=(client_sock,)).start()

if __name__ == "__main__":
    # Replace these with your virtual machine IP addresses and ports
    vm = ("0.0.0.0", 8000)

    start_chat(*vm)
