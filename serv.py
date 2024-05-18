import socket
import threading

def handle_client(client_socket, client_address):
    print(f"Подключился клиент: {client_address}")
    while True:
        try:
            message = client_socket.recv(1024).decode("utf-8")
            if message:
                print(f"Сообщение от клиента {client_address}: {message}")
                broadcast(message)
            else:
                print(f"Клиент {client_address} отключился")
                remove_client(client_socket)
                break
        except:
            print(f"Ошибка при обработке сообщения от клиента {client_address}")
            remove_client(client_socket)
            break

def broadcast(message):
    for client_socket in clients:
        try:
            client_socket.send(message.encode("utf-8"))
        except:
            print("Ошибка при отправке сообщения")

def send_message_to_all():
    while True:
        message = input("Введите сообщение для отправки всем клиентам: ")
        broadcast(message)

def remove_client(client_socket):
    if client_socket in clients:
        clients.remove(client_socket)

def start_server():
    global clients
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('10.0.2.15', 8000))
    server_socket.listen(5)

    print("Сервер чата запущен.")

    clients = []
    while True:
        client_socket, client_address = server_socket.accept()
        clients.append(client_socket)
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()

        # Start a separate thread to send messages to all clients
        send_thread = threading.Thread(target=send_message_to_all)
        send_thread.start()

start_server()
