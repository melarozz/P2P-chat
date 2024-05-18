import socket
import threading
import sys
import time
from random import randint

BROADCAST_IP = '255.255.255.255'

class Server:
    connections = []
    peers = []

    def __init__(self, port):
        self.port = port
        sck = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sck.bind((BROADCAST_IP, self.port))
        sck.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sck.listen(1)
        print("Server initialized")

        while True:
            c, a = sck.accept()
            cThread = threading.Thread(target=self.handler, args=(c, a))
            cThread.daemon = True
            cThread.start()
            self.connections.append(c)
            self.peers.append(a[0])
            print(f"{str(a[0])} : {str(a[1])} connected")
            self.send_peers()

    def handler(self, c, a):
        while True:
            data = c.recv(1024)

            for connection in self.connections:
                connection.send(data)

                if not data:
                    print(f"{str(a[0])} : {str(a[1])} disconnected")
                    self.connections.remove(c)
                    self.peers.remove(a[0])
                    c.close()
                    self.send_peers()
                    break

    def send_peers(self):
        p = ""
        for peer in self.peers:
            p = f"{p} + {peer},"

        for connection in self.connections:
            connection.send(b'\x11' + bytes(p, "utf-8"))


def send_message(sck):
    while True:
        sck.send(bytes(input("Enter a message: "), 'utf-8'))


class Client:

    def __init__(self, address, port):
        self.address = address
        self.port = port
        sck = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sck.connect((self.address, self.port))
        sck.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        thread = threading.Thread(target=send_message, args=(sck,))
        thread.daemon = True
        thread.start()

        while True:
            data = sck.recv(1024)
            if not data:
                break
            if data[0:1] == b'\x11':
                self.updatePeers(data[1:])
            else:
                print(str(data, 'utf-8'))

    def updatePeers(self, data):
        PeerToPeer.peers = str(data, "utf-8").split(",")[:-1]


class PeerToPeer:
    peers = ['10.0.2.15', '192.168.15.2']


while True:
    try:
        print("Trying to connect...")
        time.sleep(randint(1, 5))

        for peer in PeerToPeer.peers:
            try:
                client = Client(peer, 10000) # Change port number as needed
            except KeyboardInterrupt:
                sys.exit(0)
            except:
                pass

            try:
                server = Server(10000) # Change port number as needed
            except KeyboardInterrupt:
                sys.exit(0)
            except:
                print("An error occurred while trying to start the server")
    except KeyboardInterrupt:
        sys.exit(0)
