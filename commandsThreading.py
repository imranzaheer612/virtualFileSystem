from threading import Lock, Thread
from userMenu import UserRequest
import math
import logging


thread_input_file = "threads/input_thread.txt"
user = UserRequest()

# help in threading
lock = Lock()
# all the commands to be executed
commandsList = []

# this counter will take care how many commands has been executed by the pool of threads
command_being_executed = 0
thread_being_runned = 0
thread_list = list()
commands_per_thread = 0
total_commands = 0




##
# increments the shared variable among threads
# #
def inc_command_counter():
   global command_being_executed
   lock.acquire()
   command_being_executed += 1
   lock.release()


def commands_left():
    global command_being_executed, total_commands
    lock.acquire()
    if (command_being_executed >= total_commands):
        lock.release()
        return False
    lock.release()
    return True

##
# calculating no of commands per thread
# @param thread : no of thread to make --> specified by the user
# @param num_commands: no of commands available for execution
# #
def threadsCount(threads, num_commands):
    command_set = num_commands / threads
    return math.ceil(command_set)

##
# pick the available commands from the given file
# --> make threads
# #
def pickCommandFromFile(no_of_threads):
    global commandsList, commands_per_thread, total_commands

    fileRead = open(thread_input_file, 'r')
    commands_str = fileRead.read()
    commandsList = commands_str.split("\n")
    total_commands = len(commandsList)
    commands_per_thread = threadsCount(no_of_threads, total_commands)

    # print("command per thread --_++++++++++++++++++++++", commands_per_thread)
    # no_of_threads = 2
    for threads in range(no_of_threads):
        thread()

    joinThreads()


##
#@var 'command_being_executed' is a shared variable
# --> we will use it keeping in view the thread synchronization
# #
def commandSetExecution(logger, thread_name, thread_num):
    global command_being_executed, commands_per_thread, commandsList

    counter = 1
    file_name = "threads/inputThread" + str(thread_num) + ".txt"

    while(commands_left()):

        lock.acquire()
        # print("thread_name: ", thread_name, " -- commandCounter: ", command_being_executed)
        # print("thread_name: ", thread_name, "-- commands being executed per thread: ", counter)
        
        command_str = commandsList[command_being_executed]
        executable_command = command_str.split(" ")

        # store commands executed per thread in a sparate file
        if (counter == 1):
            inputFile = open(file_name, 'w')
        else:
            inputFile = open(file_name, 'a')

        # LOGGING
        log = "\n[+]Executing command by Thread: " + thread_name + " command number: " + str(command_being_executed) + " Command: " + command_str
        print(log)
        inputFile.write(log)
        logger.debug(log)

        # inc SHARED VARIABLE
        command_being_executed += 1
        lock.release()
        
        # EXECUTION
        user.execCommand(executable_command, logger)

        counter += 1
        if (counter > commands_per_thread):
            break





def thread():
    global thread_being_runned
    
    # making logger per thread
    logger_name = 'logger' + str(thread_being_runned)
    logger = logging.getLogger(logger_name)
    formatter = logging.Formatter('[%(asctime)s] : %(message)s')

    # output log file per thread
    outputFile = "threads/outputThread" + str(thread_being_runned) + ".txt"
    fileHandler = logging.FileHandler(outputFile, mode='w')
    fileHandler.setFormatter(formatter)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(fileHandler)

    # making threads
    threadName = "thread" + str(thread_being_runned)
    newThread = Thread(target=commandSetExecution, name=threadName, args=[logger, threadName, thread_being_runned],)
    thread_list.append(newThread)

    newThread.start()
    print("[+]Thread Started: ", thread_being_runned)
    thread_being_runned += 1


def joinThreads():
    global thread_list
    # wait for the thread
    for index, thread in enumerate(thread_list):
        print("thread: ", index, " - waiting")
        thread.join()
        print("thread completed: ", index)



print("Number of threads should be less than commands in the inputthread.txt file")
print("Enter the number of thread you wanna generate: ")
no_of_threads = int(input())
pickCommandFromFile(no_of_threads)