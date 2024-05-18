import socket
import threading


def receive_messages():
    while True:
        try:
            message = client_socket.recv(1024).decode("utf-8")
            if message:
                print(f"Сообщение broadcast от сервера: {message}")
        except:
            print("Ошибка при получении сообщения от сервера")
            client_socket.close()
            break


def send_message():
    while True:
        message = input()
        client_socket.send(message.encode("utf-8"))


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 9999))

receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

send_thread = threading.Thread(target=send_message)
send_thread.start()
