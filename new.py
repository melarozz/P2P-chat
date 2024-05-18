import socket
import sys
import threading

def readSocketAndOutput(s):
    global byeFlag
    print("Enter 'bye' to quit chat")
    while True:
        if byeFlag:
            try:
                str_recv = s.recv(100).decode()
                print("\r>>> " + str_recv + "\n<<<", end="", flush=True)
            except:
                print("Connection closed")
                break

            if str_recv == "bye":
                byeFlag = 0
                break
        
    print("Remote user disconnected!!!")
    s.close()
    
def readSTDINandWriteSocket(s):
    global byeFlag
    while True:
        if byeFlag:
            str_send = input("<<< ")
            s.send(str_send.encode())
            if str_send == "bye":
                print("Chat termination signal sent!!!")
                byeFlag = 0
                s.close()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
byeFlag = 1

ch = input("Connect[1] to peer or wait[2] for peer connection. Enter choice:")

if ch == "1":
    host = input("Enter peer IP:")
    port = 54321
    s.connect((host, port))
    threading.Thread(target=readSocketAndOutput, args=(s,)).start()
    threading.Thread(target=readSTDINandWriteSocket, args=(s,)).start()
    
elif ch == "2":
    host = ''
    port = 54321
    s.bind((host, port))
    s.listen(2)
    print("Waiting for connection...")
    c, addr = s.accept()  # Establish connection with client.
    threading.Thread(target=readSocketAndOutput, args=(c,)).start()
    threading.Thread(target=readSTDINandWriteSocket, args=(c,)).start()

else:
    print("Incorrect choice")
    sys.exit()
