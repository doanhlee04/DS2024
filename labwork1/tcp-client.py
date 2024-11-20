import socket 
from enum import Enum
# Creating Client Socket 

host = '127.0.0.1'
port = 8080

class Signal(Enum):
    CLOSE_SERVER = b'CLS'
    SEND_A_FILE = b'SAF'
    REQUEST_A_FILE = b'RAF'
    SEND_A_REPO = b'SAR'
    REQUEST_A_REPO = b'RAR'
    DONE = b'D1'



filename = 'cli-send.txt'

def send_signal(client_socket: socket.socket, signal:bytes ):
    client_socket.send(signal)
    pass

def send_file():

    pass

def receive_file():

    pass

def send_repo():
    
    pass

def receive_repo():

    pass

if __name__ == "__main__":
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    # Connecting with Server 
    sock.connect((host, port)) 