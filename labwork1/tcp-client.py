import socket 
from constant import *
from time import sleep
import struct
from os.path import exists, join
from os import listdir

filename = 'cli-send.txt'

def send_signal(client_socket: socket.socket, signal: Signal ):
    client_socket.send(signal.value)
    pass

def recv_signal(client_socket: socket.socket) -> bytes:
    return client_socket.recv(SIGNALSIZE)

def send_file(client_socket : socket.socket, file_name: str):
    """Send a file to server"""
    if not exists(file_name):
        raise FileNotFoundError(f'{file_name} does not exist')
    
    send_signal(client_socket, Signal.SEND_A_FILE )
    sleep(0.1)
    
    client_socket.send(file_name.split("/")[-1].encode())
    sleep(0.1)

    with open(file_name, 'rb') as f:
        while chunk := f.read(BUFFERSIZE):
            client_socket.send(chunk)

    sleep(0.1)
    send_signal(client_socket, Signal.DONE)

def request_file(client_socket : socket.socket, file_name: str, save_file=None):
    """Request a file from server"""
    if save_file is None: save_file = file_name

    send_signal(client_socket, Signal.REQUEST_A_FILE )
    sleep(0.1)
    client_socket.send(file_name.encode())
    sleep(0.1)

    response = recv_signal(client_socket)
    if response == Signal.ERROR.value:
        print("Error: File not found")
        return None
     
    with open(save_file, 'wb') as file:
        print(f"Downloading file: {file_name}")
        while True:
            data = client_socket.recv(BUFFERSIZE)
            send_signal(client_socket, Signal.PONG)

            if not data or data == Signal.DONE.value:  # End signal
                break

            file.write(data)

def send_repo(client_socket : socket.socket, repo_name: str):
    send_signal(client_socket, Signal.SEND_A_REPO )
    files = listdir(repo_name)
    
    sleep(0.1)
    # Send number of files in repo
    n_files = len(files)
    n_files = struct.pack('!I', n_files)
    client_socket.send(n_files)

    for file in files:
        sleep(0.1)
        client_socket.send(file.encode())
        sleep(0.1)

        with open(join(repo_name, file), 'rb') as f:
            while chunk := f.read(BUFFERSIZE):
                client_socket.send(chunk)

        sleep(0.1)
        send_signal(client_socket, Signal.DONE)
    
    pass

def request_repo(client_socket : socket.socket, repo_req: str, repo_save: str = r'client-receive/'):
    send_signal(client_socket, Signal.REQUEST_A_REPO )
    sleep(0.1)
    # Send repo name
    client_socket.send(repo_req.encode())

    # Get number of files in repo
    n_files = client_socket.recv(4) # 4 bytes of an int
    n_files = struct.unpack('!I', n_files)[0]
    
    print(f'number of files: {n_files}')
    for _ in range(n_files):
        file_name = client_socket.recv(BUFFERSIZE) # Get file name
        file_name = file_name.decode()
        save_file = join(repo_save, file_name)
        print(f"Downloading file: {file_name}")

        with open(save_file, 'wb') as file:
            
            while True:
                data = client_socket.recv(BUFFERSIZE)

                if not data or data == Signal.DONE.value:  # End signal
                    break

                file.write(data)

    pass

if __name__ == "__main__":
    cli_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    # Connecting with Server 
    cli_sock.connect((HOST, PORT)) 

    # region do something
    # send_file(cli_sock, r'file-transfered/client-send/send0.txt')
    # request_file(cli_sock, 'ser-send.txt', 'recv0.txt')
    # send_repo(cli_sock, r'file-transfered/client-send/')
    request_repo(cli_sock, 'file-transfered/server-send', r'file-transfered/client-receive/')
    sleep(0.1)
    send_signal(cli_sock, Signal.CLOSE_SERVER)
    # endregion