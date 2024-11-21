import socket 
import os
from constant import *
from time import sleep

def receive_file(client_socket: socket.socket, filename: str ='ser-recv.txt'):
    """Receives a file from the client."""

    with open(filename, 'wb') as file:
        print(f"Receiving file: {filename}")
        while True:
            data = client_socket.recv(BUFFERSIZE)

            if not data or data == Signal.DONE.value:  # End signal
                break
            file.write(data)

    print(f"File received: {filename}")

def send_file(client_socket: socket.socket, filename: str):
    """Sends a file to the client."""
    if os.path.exists(filename):
        print(f"Sending file: {filename}")

        with open(filename, 'rb') as file:
            while chunk := file.read(BUFFERSIZE):
                client_socket.send(Signal.PING.value)
                sleep(0.1)
                client_socket.send(chunk)

        sleep(0.1)
        client_socket.send(Signal.DONE.value)  # End signal

        print("File sent successfully.")
    else:
        client_socket.send(b'ERROR: File not found')
        print("File not found.")

def receive_signal(client_socket: socket.socket) -> bytes:
    sig = client_socket.recv(SIGNALSIZE)
    return sig


if __name__ == "__main__":
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    sock.bind((HOST, PORT)) 
    sock.listen(TOTALCLIENTS) 

    # Establishing Connections 
    client_socket, client_address = sock.accept()

    with client_socket:
        print(f"Connected by {client_address}")
        while True:
            sig = receive_signal(client_socket)
            if sig == Signal.CLOSE_SERVER.value:
                print('closing')
                break
            
            if sig == Signal.SEND_A_FILE.value:
                receive_file(client_socket)

            if sig == Signal.REQUEST_A_FILE.value:
                file_name = receive_signal(client_socket)
                send_file(client_socket, file_name.decode())
            if not sig:
                break
            print(sig.decode())
