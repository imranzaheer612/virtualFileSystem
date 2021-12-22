from DirectoryTree import DirectoryTree
from app import FileSystemFunctions
import logging
import os





class UserRequest:

    def __init__(self):
        self.appMethods =  FileSystemFunctions()
        self.tree = DirectoryTree(None)
        self.tree = self.appMethods.getDataStructure()
        # self.commandThreads = CommandThreading()


    # helper method to display help 
    def display_help(self):
        print("Commands:")
        print("    mkfile <filename>              - Make a file")
        print("    rm    <filename>               - Remove file")
        print("    mkdir <dirname>                - Make a directory")
        print("    cd    <dirname>                - Change directory")
        print("    write <filename> <string> ...  - Write string to file")
        print("    writeat <filename> <point> <string> ...- Write string to file at specific point")
        print("    append <filename> <string> ... - Append string to file")
        print("    truncate <filename> <size> ... - Truncates the file to given size")
        print("    read <filename>                - Read contents of file")
        print("    readfrom <filename> <point> <size>...- Reads the file from given point")
        print("    movewithin <filename> <from> <to> <size> ...- Move the given size content from one to other point within the file")
        print("    show                           - Show memory of root directory")
        print("    ls                             - Show self.tree of current directory")
        print("     thread_commands <no of threads>  - excute all commands in threads ")
        print("    close                          - Save and Quit")



    def execCommand(self, commands, logger):

        log = ""
        if commands[0] == "mkfile" and len(commands) == 2:
            try:
                self.appMethods.create_file(commands[1])
                log = "[+]file created successfully " + commands[1]
            except Exception as e:
                log =  "[-]an error occurred while creating the file " + commands[1]  + "\nError: "  + str(e)
            
        elif commands[0] == "rm" and len(commands) == 2:
            try:
                self.appMethods.remove_file(commands[1])
                log = "[+]file removed successfully " + commands[1]
            except Exception as e:
                log = "[-]an error occurred while removing the file " + commands[1] + "\nError: "  + str(e)

            # logging.debug(log)
                
        elif commands[0] == "write" and len(commands) > 2:
            try:
                string = " ".join(commands[2:])
                self.appMethods.write_to_file(commands[1], string, 'w')
                log = "[+]writing to the file succeeded " + commands[1]
            except Exception as e:
                log = "[-]an error occurred while writing to the file " + commands[1] + "\nError: "  + str(e)
                
                
        elif commands[0] == "append" and len(commands) > 2:
            try:
                string = " ".join(commands[2:])
                self.appMethods.write_to_file(commands[1], string, 'a')
                log = "[+]appending to the file succeeded " + commands[1]
            except Exception as e:
                log = "[-]an error occurred while appending to the file " + commands[1] + "\nError: "  + str(e)
            
        elif commands[0] == "writeat" and len(commands) > 3:
            try:
                string = " ".join(commands[3:])
                self.appMethods.write_at_file(commands[1], string, int(commands[2]))
                log = "[+]writing at to the file is successfull " + commands[1] + " at " + commands[2]
            except Exception as e:
                log = "[-]an error occurred while writing to the file " + commands[1] + "\nError: "  + str(e)

        elif commands[0] == "truncate" and len(commands) == 3:
            try:
                self.appMethods.file_truncate(commands[1], int(commands[2]))
                log = "[+]file truncating successful " + commands[1] + " truncate size: " + commands[2]
            except Exception as e:
                log = "[-]an error while truncating file " + commands[1] + "\nError: "  + str(e)

        elif commands[0] == "read" and len(commands) == 2:
            try:
                data = self.appMethods.read_file(commands[1])
                print(data)
                log = data
                log += "\n[+]reading from the file is successfull " + commands[1]
            except Exception as e:
                log = "[-]an error occurred while reading from the file " + commands[1] + + "\nError: "  + str(e)
        
        elif commands[0] == "readfrom" and len(commands) == 4:
            try:
                data = self.appMethods.read_from_file(commands[1], int(commands[2]), int(commands[3]))
                print(data)
                log = data
                log += "\n[+]reading from the file is successfull " + commands[1]
            except Exception as e:
                log = "[-]an error occurred while writing to the file " + commands[1] + "\nError: "  + str(e)
        
        elif commands[0] == "movewithin" and len(commands) == 5:
            try:
                self.appMethods.move_file_content(commands[1], int(commands[2]), int(commands[3]), int(commands[4]))
                log = "[+]moving the content in the file " + commands[1]
            except Exception as e:
                log = "[-]an error occurred while moving the content in the file " + commands[1] + "\nError: "  + str(e)

        elif commands[0] == "mkdir" and len(commands) == 2:
            try:
                self.appMethods.make_dir(commands[1])
                log = "[+]making new dir " + commands[1]
            except Exception as e:
                log = "[-]an error occurred while making new dir " + commands[1] + "\nError: "  + str(e)

        elif commands[0] == "cd" and len(commands) == 2:
            try:
                self.appMethods.changeDir(commands[1])
                log = "[+]chaning to dir " + commands[1]
            except Exception as e:
                log = "[-]an error occurred while changing to dir " + commands[1] + "\nError: "  + str(e)

        elif commands[0] == "ls":
            try:
                printed_tree = self.tree.printTree(self.tree.root)
                log = "[+]listing the directory structure successfull " +  "\n" + printed_tree

            except Exception as e:
                log = "[-]an error occurred while listing the directory tree " + "\nError: "  + str(e)

        elif commands[0] == "show":
            try:
                printed_map = self.tree.memorymap(self.tree.root)
                log = "[+]showing the memory map " + " \n" + printed_map
            except Exception as e:
                log = "[-]an error occurred while showing the memory map " + e

        # elif commands[0] == "thread_commands" and len(commands) == 2:
        #     self.commandThreads.pickCommandFromFile(commands[1], self.execCommand)
            

        print(log)
        logger.debug(log)



    # main class to begin the execution
    def userInput(self):
        userLog = logging.getLogger("userLogger")
        userLog.setLevel(logging.DEBUG)

        # print(f"Operating System - Lab 06")
        print(f"Type help to display list of commands")

        while True:
            print(f"{self.tree.root.dir.name} />>> ", end="")
            command_str = input()
            commands = command_str.split(" ")
            self.execCommand(commands, userLog)

            if commands[0] == "help":
                self.display_help()
                continue

            elif commands[0] == "close":
                # update_file(root)
                break

            else:
                print(f"Wrong command: {commands[0]}, type \"help\" for more information")

    # initiating main function
    # if _name_ == "_main_":
    # main()


# sampleUser = UserRequest()
# sampleUser.userInput()

