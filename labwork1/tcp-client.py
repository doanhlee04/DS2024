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

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
# Connecting with Server 
sock.connect((host, port)) 

filename = 'cli-send.txt'
try: 
# Reading file and sending data to server 
    fi = open(filename, "r") 
    data = fi.read() 
    if not data: 
        exit
    while data: 
        sock.send(str(data).encode()) 
        data = fi.read() 

    # File is closed after data is sent 
    fi.close() 

except IOError: 
    print('You entered an invalid filename!\nPlease enter a valid name') 
