import os
from threading import Lock, Thread
from execution import Executor
import logging
import socket
from pathlib import Path
import os


executor = Executor()
lock = Lock()
thread_being_runned = 0
port = 1234


absolute_path = Path().absolute()
tempResultFile = os.path.join(absolute_path, "threads/tempResult.txt")
# tempResultFile = os.path.relpath(absolute_path)
# tempResultFile = pathlib.Path().resolve()
# tempResultFile = os.path.join(tempResultFile, "/threads/tempResult.txt")



#
# make a new socket for each client
#  #
def readyServer():
    global port, thread_being_runned

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    host = socket.gethostname()
    print('[+]Server will start on host : ', host)
    print("[+]Server is waiting on")
    print("port: ", port)
    s.bind(('', port))
    print()
    print('[!]Waiting for new client')
    print()

    s.listen(1)
    conn, addr = s.accept()
    if (addr):
        clientThreadName = addr
        thread_being_runned += 1
        newClientThread = Thread(target=serveNewClient, name=clientThreadName, args=[conn, addr],)
        newClientThread.start()

        Thread(target=readyServer, name="newWait", args=[]).start()



def serveNewClient(conn, addr):
    global port
    print(addr, ' Has connected to the server')
    print()

    # INIT
    global thread_being_runned
    
    # making logger per thread
    logger_name = 'logger' + str(thread_being_runned)
    logger = logging.getLogger(logger_name)
    formatter = logging.Formatter('[%(asctime)s] : %(message)s')

    # output log file per thread
    outputFile = "threads/outputClient" + str(thread_being_runned) + ".txt"
    fileHandler = logging.FileHandler(outputFile, mode='w')
    fileHandler.setFormatter(formatter)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(fileHandler)

    #inputfile
    file_name = "threads/inputClient" + str(thread_being_runned) + ".txt"
    inputFile = open(file_name, 'w')

    while 1:
        inputFile = open(file_name, 'a')
        incoming_message = conn.recv(5000)
        incoming_message = incoming_message.decode()
        inputFile.write("\nExecuting command: " + incoming_message)
        if (incoming_message == 'close'):
            break

        my_commands = incoming_message.split(" ")
        executor.execCommand(my_commands, logger)

        lock.acquire()
        log_file = open(tempResultFile,"r")
        message = log_file.read()
        # message += "\n[Current Dir]: " + executor.currentDirName
        log_file.close
        lock.release()

        message = message.encode()
        inputFile.close()

        # close connection if client crashes unexpectedly
        try:
            conn.send(message)
        except socket.error:
            conn.close()
            break








readyServer()

