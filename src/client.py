from DirectoryTree import DirectoryTree
from app import FileSystemFunctions
import logging
import os
import socket




s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "127.0.0.1"
port = 1234
s.connect((host, port))
print('[+]Connected to file server')
while 1:
    message = input(str('>> '))
    if (message == 'close'):
        message = message.encode()
        s.send(message)
        break
    message = message.encode()
    s.send(message)

    incoming_message = s.recv(5000)
    incoming_message = incoming_message.decode()
    print(incoming_message)
