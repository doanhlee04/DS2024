import socket
import pickle
import os
# Server configuration
HOST = '127.0.0.1'
PORT = 5000

def rpc_call(method, params):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((HOST, PORT))
        data = {'method': method, 'params': params}
        client_socket.sendall(pickle.dumps(data))
        response = pickle.loads(client_socket.recv(4096))
        return response

def upload_file(filepath):
    filename = filepath.split('/')[-1]
    with open(filepath, 'rb') as f:
        file_data = f.read()
    response = rpc_call('upload', {'filename': filename, 'data': file_data})
    print(response)

def download_file(filename, save_path):
    response = rpc_call('download', {'filename': filename})
    if response['status'] == 'success':
        with open(save_path, 'wb') as f:
            f.write(response['data'])
        print(f"{filename} downloaded to {save_path}")
    else:
        print(response)

if __name__ == "__main__":
    upload_file(r"C:\Users\HG\Downloads\hoctap\Distributed-System\DS2024\labwork2\file-transfered\client_files\dummy1.txt")


   