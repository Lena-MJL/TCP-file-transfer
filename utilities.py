# Utility funcitons to be used by client.py and server.py
# Authors - Magdalena Latifa 2398248l and Ivan Nikitin 2292523n
# Lab group LB10
import socket
import sys
import os
from os import listdir
from os.path import curdir


def send_file(socket, file_name):
    """
    Opens the file with the given file name and sends its data over networwk
    Args:
        param1(socket): The socket.
        param2 (str): The file name.
    Raises:
        OSError if can not establish connection
        IOError if encounters errors with file
    """
    print("Sending:", file_name)
    try:
        with open(file_name, 'rb') as f:
            raw = f.read()
    except IOError:
        print("There was an error openning the file, make sure it exists.")
        return

    # Send actual length ahead of data, fix byteorder and size
    try:
        socket.sendall(len(raw).to_bytes(8, 'big'))
        # No need to chunk as we have it all in memory
        socket.sendall(raw)
        print('Sent')
    except OSError as e:
        print('Cannot establish connection during sending' + str(e))
        return


def recv_file(socket, file_name):

    """
    Creates file with given name and stores data recieved from socket
    Args:
        param1(socket): The socket.
        param2(str): The file name.
    Raises:
        OSError if can not establish connection
        IOError if encounters errors with file
    """
    # Get the expected length which will always be 8 bytes
    print('Accepting' + file_name)
    expected_size = b""
    while len(expected_size) < 8:
        try:
            more_size = socket.recv(8 - len(expected_size))
            expected_size += more_size
        except OSError as e:
            print('Cannot establish connection during receiving' + str(e))
            break

    # the expected file length
    expected_size = int.from_bytes(expected_size, 'big')

    # keep receiving until we reach expected length of file
    packet = b""
    while len(packet) < expected_size:
        try:
            buffer = socket.recv(expected_size - len(packet))
        except OSError as e:
            print('Cannot establish connection during receiving' + str(e))
            sys.exit(1)
        if not buffer:
            raise Exception("Incomplete file received")
        packet += buffer

    try:
        with open(file_name, 'xb') as f:
            f.write(packet)
            print('File received')
    except IOError:
        print("There was en error with writing to the file.")
        sys.exit(1)


def send_listing(socket, file_name):
    """
    Generates and sends the directory listing from the server to the client
    Args:
        param1(socket): The socket
        param2(file): redundant but used for consistancy of calls
    Raises:
        OSError if can not establish connection
        IOError if encounters errors with directory listing
    """
    print("Sending:", file_name)
    try:
        data = '\n'.join(listdir(os.path.curdir))
    except IOError:
        print("There was an error reading the directories.")
        sys.exit(1)

    # Send actual length ahead of data, fix byteorder and size
    try:
        socket.sendall(len(data).to_bytes(8, 'big'))
        # No need to chunk as we have it all in memory
        socket.sendall(str.encode(data))
        print('Sent listing')
    except OSError as e:
        print('Cannot establish connection during sending' + str(e))
        sys.exit(1)


def recv_listing(socket, file_name):

    """
    Receives the listing from the server and prints it on the screen
    Args:
        param1(socket): The socket
        param2(file): redundant but used for consistancy of calls
    Raises:
        OSError if can not establish connection
        IOError if encounters errors with directory listing
    """
    expected_size = b""
    while len(expected_size) < 8:
        try:
            more_size = socket.recv(8 - len(expected_size))
            expected_size += more_size
        except OSError as e:
            print('Cannot establish connection during receiving' + str(e))
            sys.exit(1)

    # the expected file length
    expected_size = int.from_bytes(expected_size, 'big')

    # keep receiving until we reach expected length of directory listing
    packet = b""
    while len(packet) < expected_size:
        try:
            buffer = socket.recv(expected_size - len(packet))
        except OSError as e:
            print('Cannot establish connection during receiving' + str(e))
            sys.exit(1)
        if not buffer:
            raise Exception("Incomplete directory listing received")
        packet += buffer
    data = packet.decode()
    print(data + '\n')
