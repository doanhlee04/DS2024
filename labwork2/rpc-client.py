import socket
import pickle
import os
# Server configuration
HOST = '127.0.0.1'
PORT = 5000
client_dir = r"C:\Users\HG\Downloads\hoctap\Distributed-System\DS2024\labwork2\file-transfered\client_files"
save_dir = r"C:\Users\HG\Downloads\hoctap\Distributed-System\DS2024\labwork2\file-transfered\client_files"
def rpc_call(method, params):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((HOST, PORT))
        data = {'method': method, 'params': params}
        client_socket.sendall(pickle.dumps(data))
        response = pickle.loads(client_socket.recv(4096))
        return response

def upload_file(filename):
    # Construct the full file path
    filepath = os.path.join(client_dir, filename)
    # Read and send the file
    with open(filepath, 'rb') as f:
        file_data = f.read()
    response = rpc_call('upload', {'filename': filename, 'data': file_data})
    print(response)
def download_file(filename):
    # Call the 'download' RPC method on the server
    response = rpc_call('download', {'filename': filename})
    if response['status'] == 'success':
        # Full path to save the file
        save_path = os.path.join(save_dir, filename)     
        # Save the file content
        with open(save_path, 'wb') as f:
            f.write(response['data'])
        print(f"{filename} downloaded successfully to {save_path}")
    else:
        print(f"Error: {response['message']}")

if __name__ == "__main__":
    download_file("dummy2.txt")


   