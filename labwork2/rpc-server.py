import json
import socket
import inspect
from threading import Thread
import warnings

# rpc.py
class RPCServer:
    def __init__(self, host:str='127.0.0.1', port:int=8080) -> None:
        self.host = host
        self.port = port
        self.address = (host, port)
        self._methods = {}

    def register_method(self, func) -> None:
        if not callable(func):
            raise Exception("Adding a non function object is not allowed")
        self._methods.update({func.__name__ : func})

class RPCClient:
    def __init__(self) -> None:
        pass

    def __str__(self) -> str:
        return "A client"

if __name__ == '__main__':
    test_server = RPCServer()
    
    test_server.register_method(RPCServer)
