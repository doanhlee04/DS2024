import socket 
import os
from constant import *
from time import sleep
import struct
from mpi4py import MPI

def recv_signal(comm):
    signal = comm.recv(source=MPI.ANY_SOURCE)
    if isinstance(signal, Signal):  # Ensures it's a signal
        return signal
    else:
        raise ValueError(f"Expected signal, got {type(signal)}")

def receive_file(comm, source, dest_path):
    signal = comm.recv(source=source)  # Expecting a signal like SEND_A_FILE
    print(signal)
    if signal != b'SAF':
        print(f"Unexpected signal: {signal}")
        return
    '''Receive file from a remote process and save it to dest_path'''
    file_name = comm.recv(source=source)
    file_size = comm.recv(source=source)
    print(f"Receiving file: {file_name} ({file_size} bytes)")
    # Receive the file content
    with open(dest_path + file_name, 'wb') as file:
        received_bytes = 0
        while received_bytes < file_size:
            chunk = comm.recv(source=source)  # Receive file chunks from the same source
            if chunk == Signal.DONE:
                break
            file.write(chunk)
            received_bytes += len(chunk)
        print(f"File {file_name} received successfully.")

def send_signal(comm, signal, dest):
    """Send a signal to a specific destination."""
    comm.send(signal.value, dest=dest)

def send_file(
        comm,dest,file_path
        ) -> None:
    '''gui file den dia diem process'''
    if not os.path.exists(file_path):
        print(f'file not found')
        comm.send(Signal.ERROR, dest=dest)
        return 
    file_name=os.path.basename(file_path)
    file_size=os.path.getsize(file_path)
    print(f'sending file: {file_name} ({file_size} bytes) !!!')

    comm.send(file_name,dest=dest)
    comm.send(file_size,dest=dest)
    '''gui file di'''
    with open(file_path, 'rb') as file:
        while chunk := file.read(BUFFERSIZE):
            comm.send(chunk, dest=dest)
        
    comm.send(Signal.DONE,dest=dest)
    print(f"file sent: {file_path}")

def receive_repo(comm,source,dest_path) -> None:
    """Receive a repository sent by client"""
    
    # lay file tu source
    n_files = comm.recv(source=source)
    print(f'receiving repotory with {n_files} files!')

    for _ in range(n_files):
        receive_file(comm,source,dest_path)

def send_repo(
        comm, dest, repo_path
        ) -> None:
    """Send a repository to client"""   
    if not os.path.exists(repo_path):
        print("repotory not found")
        comm.send(Signal.ERROR,dest=dest)
        return
    files = os.listdir(repo_path)
    comm.send(len(files),dest=dest)
    for file_name in files:
        send_file(comm,dest,os.path.join(repo_path,file_name))


def main():
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
    print(f"Rank: {rank}, Size: {size}")

    if rank == 0:  # Server
        while True:
            # Receive the signal first
            signal = comm.recv(source=MPI.ANY_SOURCE)
            source = comm.recv(source=MPI.ANY_SOURCE)
            print(f"Received signal: {signal}, from source: {source}")

            if signal == Signal.CLOSE_SERVER:
                print("Shutting down server.")
                break
            elif signal == Signal.SEND_A_FILE:
                # Now, expect the file name
                receive_file(comm, source, dest_path=r'file-transfered/server-receive/')
            elif signal == Signal.REQUEST_A_FILE:
                print("Signal received: REQUEST_A_FILE")
                file_path = comm.recv(source=source)
                send_file(comm, source, file_path)
            elif signal == Signal.SEND_A_REPO:
                print("Signal received: SEND_A_REPO")
                receive_repo(comm, source, dest_path=r'file-transfered/server-receive/')
            elif signal == Signal.REQUEST_A_REPO:
                print("Signal received: REQUEST_A_REPO")
                repo_path = comm.recv(source=source)
                send_repo(comm, source, repo_path)

        print("Server process terminated.")
        MPI.Finalize()

main()