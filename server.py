# server.py file for NOSE assessed exercise 1
# Authors - Magdalena Latifa 2398248l and Ivan Nikitin 2292523n
# Lab group LB10
"""
Purpose of server.py:
    upload a file (request type and the filename -- exclusive binary mode)
    download a file (open the file in binary mode)
    list 1st level directory contents

print reoprt on the console after a request was processed
"""

import sys
import socket
import os

# Define hostname and get port from user
HOST = '0.0.0.0'
if len(sys.argv) != 2:
    print('Expected two arguments - server file and port number')
try:
    PORT = int(sys.argv[1])
except ValueError:
    print("Invalid argument - int expected")


# Define socket, bind to specified port, on request ping back address
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST,PORT))
    print('Server up and running.')
    s.listen(5)
    conn, addr = s.accept()
    with conn:
        while True:
            data = conn.recv(1024).decode('utf-8')
            print(str(addr) + ": " + data)
            myfile = open(data, "xb")
            if not data:
                break
        print('Done recieving file')
        conn.sendall(data)
