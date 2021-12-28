from DirectoryTree import DirectoryTree
from app import FileSystemFunctions
import logging


class Executor:

    def __init__(self):
        self.appMethods =  FileSystemFunctions()
        self.tree = DirectoryTree(None)
        self.tree = self.appMethods.getDataStructure()
        self.appMethods.changeDir("testFile")
        self.currentDirName = self.tree.root.dir.name
        # self.commandThreads = CommandThreading()



    # helper method to display help 
    def display_help(self):
        help = "Commands:"
        help += "\n    mkfile <filename>              - Make a file"
        help += "\n    rm    <filename>               - Remove file"
        help += "\n    mkdir <dirname>                - Make a directory"
        help += "\n    cd    <dirname>                - Change directory"
        help += "\n    write <filename> <string> ...  - Write string to file"
        help += "\n    writeat <filename> <point> <string> ...- Write string to file at specific point"
        help += "\n    append <filename> <string> ... - Append string to file"
        help += "\n    truncate <filename> <size> ... - Truncates the file to given size"
        help += "\n    read <filename>                - Read contents of file"
        help += "\n    readfrom <filename> <point> <size>...- Reads the file from given point"
        help += "\n    movewithin <filename> <from> <to> <size> ...- Move the given size content from one to other point within the file"
        help += "\n    show                           - Show memory of root directory"
        help += "\n    ls                             - Show self.tree of current directory"
        help += "\n     thread_commands <no of threads>  - excute all commands in threads "
        help += "\n    close                          - Save and Quit"
        return help


    #
    # @param commands: give the string commads
    # @param logger: give the logger object to log the execution og the commands
    # #

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
                    # print(data)
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
                    self.currentDirName = self.tree.root.dir.name
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


            elif commands[0] == "help":
                log = self.display_help()

            else:
                log = "Wrong command: {" + commands[0] + "}, type \"help\" for more information";
            
            logger.debug(log)
            log_file = open("result.txt","w")
            log_file.write(log)
            log_file.close



