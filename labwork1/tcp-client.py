import socket 
from constant import *
from time import sleep
from os.path import exists, join

filename = 'cli-send.txt'

def send_signal(client_socket: socket.socket, signal: Signal ):
    client_socket.send(signal.value)
    pass

def recv_signal():
    pass

def send_file(client_socket : socket.socket, file_name: str):
    if not exists(file_name):
        raise FileNotFoundError(f'{file_name} does not exist')
    
    send_signal(client_socket, Signal.SEND_A_FILE )
    sleep(0.1)
    
    with open(file_name, 'rb') as f:
        while chunk := f.read(BUFFERSIZE):
            client_socket.send(chunk)

    send_signal(client_socket, Signal.DONE)


def receive_file(client_socket : socket.socket, file_name: str):
    send_signal(client_socket, Signal.REQUEST_A_FILE )
    pass

def send_repo(client_socket : socket.socket, repo_name: str):
    send_signal(client_socket, Signal.SEND_A_REPO )
    pass

def receive_repo(client_socket : socket.socket, repo_name: str):
    send_signal(client_socket, Signal.REQUEST_A_REPO )
    pass

if __name__ == "__main__":
    cli_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    # Connecting with Server 
    cli_sock.connect((HOST, PORT)) 

    send_file(cli_sock, 'cli-send.txt')
    sleep(0.1)
    send_signal(cli_sock, Signal.CLOSE_SERVER)