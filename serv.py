import socket

def get_env(key, default_val):
    return os.getenv(key, default_val)

def start_listener(ip):
    p = bytearray(2048)
    addr = ('', 8080)  # Listening on all interfaces
    ser = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ser.bind(addr)
    start_sender(ser)
    while True:
        listen(ser, p)

def start_sender(conn):
    while True:
        host, message = input_message()
        if host == "all":
            host = "255.255.255.255"
        send_message(host, message, conn)

def send_message(addr, message, conn):
    addr_ = (addr, 8080)
    conn.sendto(message.encode(), addr_)

def input_message():
    input_text = input("Message: ")
    split_input = input_text.split(" ")
    host, message = split_input[0], " ".join(split_input[1:])
    return host, message

def listen(ser, p):
    data, remote = ser.recvfrom(2048)
    print(f"New message from {remote}: {data.decode()}")
    print("Message: ")

if __name__ == "__main__":
    host = get_env("HOST", "0.0.0.0")
    start_listener(host)
    print(f"Listener started at port 8080 on host {host}")
