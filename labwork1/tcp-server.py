import socket 
import os
from constant import *
from time import sleep
import struct

def receive_signal(client_socket: socket.socket) -> bytes:
    sig = client_socket.recv(SIGNALSIZE)
    return sig

def send_signal(client_socket: socket.socket, signal: Signal):
    client_socket.send(signal.value)

def receive_file(client_socket: socket.socket, file_name: str = None):
    """Receives a file from the client."""

    # Get file name from client side
    clif_name = client_socket.recv(BUFFERSIZE)
    clif_name = clif_name.decode()
    if file_name is None: file_name = clif_name

    with open(file_name, 'wb') as file:
        print(f"Receiving file: {clif_name}")
        while True:
            data = client_socket.recv(BUFFERSIZE)

            if not data or data == Signal.DONE.value:  # End signal
                break
            file.write(data)

    print(f"File received: {file_name}")

def send_file(client_socket: socket.socket, file_name: str) -> None:
    """Sends a file to the client."""
    if os.path.exists(file_name):
        print(f"Sending file: {file_name}")

        with open(file_name, 'rb') as file:
            while chunk := file.read(BUFFERSIZE):
                send_signal(client_socket, Signal.PING)
                sleep(0.1)
                client_socket.send(chunk)

        sleep(0.1)
        send_signal(client_socket, Signal.DONE)  # End signal

        print("File sent successfully.")
    else:
        client_socket.send(b'ERROR: File not found')
        print("File not found.")

def receive_repo(client_socket: socket.socket, save_folder: str = r'received-file/') -> None:
    """Receive a repository sent by client"""
    
    # Get number of files in repo
    n_files = client_socket.recv(4) # 4 bytes of an int
    n_files = struct.unpack('!I', n_files)[0]
    
    for i in range(n_files):

        pass
    pass

if __name__ == "__main__":
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    sock.bind((HOST, PORT)) 
    sock.listen(TOTALCLIENTS) 

    # Establishing Connections 
    client_socket, clar = sock.accept()

    with client_socket:
        print(f"Connected by {clar}")
        while True:
            sig = receive_signal(client_socket)
            if sig == Signal.CLOSE_SERVER.value:
                print('closing')
                break
            
            if sig == Signal.SEND_A_FILE.value:
                receive_file(client_socket, file_name=r'file-transfered/server-receive/recv0.txt')

            if sig == Signal.REQUEST_A_FILE.value:
                file_name = receive_signal(client_socket)
                send_file(client_socket, file_name.decode())

            if sig == Signal.SEND_A_REPO.value:
                receive_repo(client_socket, r'file-transfered/server-receive/')

            if not sig:
                break
            print(sig.decode())
