from constant import *
from time import sleep
import struct
from os.path import exists, join
from os import listdir
from mpi4py import MPI
import os
filename = 'cli-send.txt'

def send_signal(comm, signal, dest ):
    comm.send(signal.value, dest=dest)

def recv_signal(comm, source) -> bytes:
    return comm.recv(source=source)

def send_file(
        comm , file_path,dest
        ) -> None:
    '''Send file to the destination process'''
    if not os.path.exists(file_path):
        print(f'File not found')
        comm.send(Signal.ERROR, dest=dest)
        return 
    
    file_name = os.path.basename(file_path)
    file_size = os.path.getsize(file_path)
    print(f'Sending file: {file_name} ({file_size} bytes)')

    # Send file start signal and details
    comm.send(Signal.SEND_A_FILE, dest=dest)
    sleep(0.1)
    comm.send(file_name.encode(), dest=dest)  # Send file name
    comm.send(file_size, dest=dest)  # Send file size
    sleep(0.1)

    # Send file content
    with open(file_path, 'rb') as file:
        while chunk := file.read(BUFFERSIZE):
            comm.send(chunk, dest=dest)
        
    comm.send(Signal.DONE, dest=dest)
    print(f"File sent: {file_name}")

def request_file(comm, file_name, dest, save_file=None):
    """Request a file from the server."""
    if save_file is None:
        save_file = file_name

    send_signal(comm, Signal.REQUEST_A_FILE, dest)
    sleep(0.1)

    # Send file name
    comm.send(file_name.encode(), dest=dest)
    sleep(0.1)

    # Receive response
    response = recv_signal(comm, dest)
    if response == Signal.ERROR:
        print("Error: File not found")
        return

    # Save the file
    with open(save_file, 'wb') as file:
        while True:
            data = comm.recv(source=dest)

            if data == Signal.DONE:
                break

            file.write(data)

def send_repo(comm, repo_name, dest):
    """Send a repository to the server."""
    if not os.path.exists(repo_name):
        raise FileNotFoundError(f'{repo_name} does not exist')

    send_signal(comm, Signal.SEND_A_REPO, dest)
    sleep(0.1)

    files = os.listdir(repo_name)

    # Send number of files
    n_files = len(files)
    comm.send(n_files, dest=dest)

    for file in files:
        sleep(0.1)

        # Send file name
        comm.send(file, dest=dest)
        sleep(0.1)

        # Send file content
        with open(os.path.join(repo_name, file), 'rb') as f:
            while chunk := f.read(BUFFERSIZE):
                comm.send(chunk, dest=dest)

        # Send end signal
        sleep(0.1)
        send_signal(comm, Signal.DONE, dest)

def request_repo(comm, repo_req, dest, repo_save):
    """Request a repository from the server."""
    send_signal(comm, Signal.REQUEST_A_REPO, dest)
    sleep(0.1)

    # Send repo name
    comm.send(repo_req, dest=dest)

    # Receive number of files
    n_files = comm.recv(source=dest)
    print(f'Number of files: {n_files}')

    for _ in range(n_files):
        # Receive file name
        file_name = comm.recv(source=dest)
        save_file = os.path.join(repo_save, file_name)
        print(f"Downloading file: {file_name}")

        # Save file content
        with open(save_file, 'wb') as file:
            while True:
                data = comm.recv(source=dest)

                if data == Signal.DONE.value:
                    break

                file.write(data)

if __name__ == "__main__":
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
    print(f"Client Rank: {rank}, Total Clients: {size}")

    SERVER_RANK = 0  # Assuming the server runs on rank 0

    try:
        # Uncomment desired operation
        send_file(comm, 'file-transfered/client-send/send0.txt', SERVER_RANK)
        #request_file(comm, "send0.txt", SERVER_RANK, 'file-transfered/client_rec/send0.txt')
        #send_repo(comm, "client-repo/", SERVER_RANK)
        #request_repo(comm, 'file-transfered/server-send', SERVER_RANK, 'file-transfered/client-receive/')
    except Exception as e:
        print(f"Error: {e}")

    # Close the server
    send_signal(comm, Signal.CLOSE_SERVER, SERVER_RANK)
    MPI.Finalize()