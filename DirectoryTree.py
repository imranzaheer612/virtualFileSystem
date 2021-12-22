
import os
from pathlib import Path
from posixpath import pardir

class File:
    def __init__(self, name, path):
        self.name = name
        self.path = path
        self.dir_name = None
        self.size = None
        self.protection = False

class Dir:
    def __init__(self, name, path):
        self.name = name
        self.path = path


class Node:
    def __init__(self):
        self.file = None  
        self.dir = None        
        self.parent = None
        self.children = []


class DirectoryTree:

    def __init__(self, curDirNode) :
        self.root = Node()
        self.root.dir = curDirNode
        # self.currentNode = self.root
        self.loc = self.root
        self.preloc = None
        self.tree_str = ""
        self.memory_map_str = ""

    def addNode(self, data, check=0):
        # if file then simply add to current dir
        parent = os.path.dirname(data.path)
        if (parent == self.loc.dir.path):

            if (isinstance(data, File)):
                newNode = Node()
                newNode.file = data
                self.loc.children.append(newNode)
            
            # if dir 
            else:
                if (parent == self.loc.dir.path):
                    newNode = Node()
                    newNode.dir = data
                    self.loc.children.append(newNode)
                
        else:
            if (check < 1):
                self.changeDir(parent)
                self.addNode(data, check + 1)
            else:
                print("[-]canont find dir: ", parent)
  
    ##
    # while finding the dir and sub_dir
    # we have to change the directory that have been
    # scanned
    # --> this will change the pointer the given dir
    # #
    def changeDir(self, dir_path):
        self.loc = self.root
        self.recursiveDirSearch(dir_path)

    def recursiveDirSearch(self, dir_path):
        if (dir_path == self.root.dir.path):
            self.loc = self.root
            return


        found = False

        dir_name = os.path.basename(dir_path)
        path = dir_path.split("/")

        # excluding irrelevant path dirs
        reqPath = path.pop(0)
        if (reqPath == "." or reqPath == ""):
            reqPath = path.pop(0)

        # finding the relevant dir
        for node in self.loc.children:
            if (node.dir):
                if (node.dir.name == reqPath):
                    self.loc = node
                    if ((len(path) == 0) and (node.dir.name == dir_name)):
                        found = True
                        # print("Found dir: ", self.loc.dir.path)
                        # self.loc = node
                        break

                    newPath = ""
                    for dir in path:
                        newPath  = newPath + "/" + dir
                    
                    if (self.recursiveDirSearch(newPath)):
                        found = True
                        break
           
        if (not found):
            return None


    ##
    # search the file in the dirs
    # if not found --> show error
    # #

    def openFile(self, file_path):
        self.preloc = None
        self.loc = self.root
        # file_path = os.path.join(self.root.dir.path, file_path)
        return self.searchFile(file_path)
        


    def searchFile(self, file_path):
        found = False
        file_name = os.path.basename(file_path)

        path = file_path.split("/")        
        reqPath = path.pop(0)

        # excluding non-realted file names
        if (reqPath == "" or reqPath == "."):
            reqPath = path.pop(0)

        # finding the right dirs to follow the path
        for node in self.loc.children:
            if (node.dir):
                if (node.dir.name == reqPath):

                    self.loc = node
                    newPath = ""
                    for dir in path:
                        newPath  = newPath + "/" + dir

                    if(self.searchFile(newPath)):
                        found = True
                    break
            
            elif (node.file):
                if (node.file.name == file_name):
                    self.preloc = self.loc
                    self.loc = node
                    found = True
                    break
        
        if (not found):
            return None
        return self.loc

    ##
    # Scanning all the dirs and sub_dirs
    # and adding them to directoryTree
    # #
    def scan_dirs(self, dirPath):
        subfolders = []
        #scanning dirs in current dir
        subfolders = [f.path for f in os.scandir(dirPath) if f.is_dir()]
        for foldersPath in subfolders:
            newDir = Dir(os.path.basename(foldersPath), foldersPath)
            self.addNode(newDir)

        # scanning files in current dir
        lst = os.listdir(dirPath)
        for element in lst:
            file_path = os.path.join(dirPath, element)
            
            if os.path.isfile(file_path):
                size = os.path.getsize(file_path)
                dir_name = os.path.dirname(file_path)

                newFile = File(element, file_path)
                newFile.size = size
                newFile.dir_name = dir_name
                self.addNode(newFile)

        # repeat the process for sub dirs if any
        for dirPath in subfolders:
            self.loc = self.root
            self.changeDir(dirPath)
            self.scan_dirs(dirPath)

        return subfolders

    def printTree(self, node):
        self.tree_str = ""
        self.tree_str += "\n<-- Printing Scanned Dirs -->\n"
        self.recursivePrint(node)
        self.tree_str += "\n<-- End -->\n"
        return self.tree_str


    def recursivePrint(self, node, level=0):
        if node:
            if (node.file):
                self.tree_str += "|--" * level + " " + node.file.name + "\n"
            else:
                self.tree_str += "|--" * level + " " + node.dir.name + "\n"

            for child in node.children:
                self.recursivePrint(child, level + 1)

    def memorymap(self, node):
        self.memory_map_str = ""
        self.recursive_memorymap(node)
        return self.memory_map_str



    def recursive_memorymap(self, node, level=0):
        if node:
            if (node.file):
                self.memory_map_str += "\n|-----------------------------"
                self.memory_map_str += "\n|--> FILE_NAME: " + node.file.name
                self.memory_map_str += "\n|--> PATH: " + node.file.path
                self.memory_map_str += "\n|--> SIZE: " + str(node.file.size)
                self.memory_map_str += "\n|--> DIR: " + node.file.dir_name

            else:
                self.memory_map_str += "\n|-----------------------------"
                self.memory_map_str += "\n|--> DIR_NAME: " + node.dir.name
                self.memory_map_str += "\n|--> PATH: " + node.dir.path

            for child in node.children:
                self.recursive_memorymap(child, level + 1)


