import os
import pickle
import socket

# Server configuration
HOST = '127.0.0.1'
PORT = 5000

# Directory where uploaded files will be saved
SERVER_DIR = r"C:\Users\HG\Downloads\hoctap\Distributed-System\DS2024\labwork2\file-transfered\server_files"

# Ensure the directory exists
os.makedirs(SERVER_DIR, exist_ok=True)

def save_file(filename, file_data):
    """Save the uploaded file to the server directory."""
    try:
        file_path = os.path.join(SERVER_DIR, filename)
        with open(file_path, 'wb') as f:
            f.write(file_data)
        print(f"File saved successfully: {file_path}")
    except Exception as e:
        print(f"Error saving file: {e}")

def handle_client(conn):
    """Handle client requests."""
    try:
        data = pickle.loads(conn.recv(4096))
        method = data.get('method')
        params = data.get('params')

        if method == 'upload':
            filename = params['filename']
            file_data = params['data']
            save_file(filename, file_data)
            response = {'status': 'success', 'message': f"{filename} uploaded"}
        else:
            response = {'status': 'error', 'message': 'Invalid method'}

        conn.sendall(pickle.dumps(response))
    except Exception as e:
        print(f"Error handling client: {e}")
    finally:
        conn.close()

def start_server():
    """Start the server."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen(5)
        print(f"Server listening on {HOST}:{PORT}")

        while True:
            conn, addr = server_socket.accept()
            print(f"Connected by {addr}")
            handle_client(conn)

if __name__ == "__main__":
    start_server()
