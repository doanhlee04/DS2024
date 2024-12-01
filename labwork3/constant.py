from enum import Enum
from sys import getsizeof

# HOST = '127.0.0.1'
# PORT = 8080
# TOTALCLIENTS = 1
BUFFERSIZE = 1024

class Signal(Enum):
    CLOSE_SERVER = b'CLS'
    SEND_A_FILE = b'SAF'
    REQUEST_A_FILE = b'RAF'
    SEND_A_REPO = b'SAR'
    REQUEST_A_REPO = b'RAR'
    DONE = b'DON'
    ERROR = b'ERR'
    PING = b'PIN'
    PONG = b'PON'

SIGNALSIZE = getsizeof(Signal.CLOSE_SERVER.value)