from time import time
from DirectoryTree import File, Dir, DirectoryTree

from pathlib import Path
from os import error, truncate, walk
import os
from posixpath import basename, dirname, join
import shutil
from typing import List
from threading import Lock,  Thread
import logging
import math
# from os import error





##
# TEST CASES
# #
class FileSystemFunctions:

    def __init__(self):
        self.absolute_path = Path().absolute()
        self.currentPath = os.path.relpath(self.absolute_path)
        self.rootDir = Dir(self.currentPath, self.currentPath)

        # making DS for files
        self.tree = DirectoryTree(self.rootDir)
        self.tree.scan_dirs(self.currentPath)

    
    def create_file(self, file_path):
        self.tree.loc = self.tree.root
        full_path = os.path.join(self.currentPath, file_path)
        open(full_path, 'x')

        newFile = File(os.path.basename(file_path), full_path)
        newFile.dir_name = os.path.dirname(file_path)
        self.tree.addNode(newFile)


    def write_to_file(self, file_path, text, mode):

        node = self.tree.openFile(os.path.join(file_path))
        full_file_path = os.path.join(self.currentPath, file_path)

        # busy waiting
        while(node.file.protection):
            pass
        
        #apply protection
        node.file.protection = True
        if (mode == 'w' ):
            fileWrite = open(full_file_path, 'w')
        
        elif (mode == 'a'):
            fileWrite = open(os.path.join(self.currentPath, file_path), 'a')

        fileWrite.write(text)
        fileWrite.close
        node.file.size = os.path.getsize(full_file_path)
        
        #remove protection
        node.file.protection = False
        

    def write_at_file(self, file_name, text, location):
        
        file_node = self.tree.openFile(file_name)
        # busy waiting
        while(file_node.file.protection):
            pass
        
        #apply protection
        file_node.file.protection = True

        #operations
        fileWrite = open(file_node.file.path, 'r+')
        fileWrite.seek(location, 0)
        fileWrite.write(text)
        fileWrite.close

        #remove protection
        file_node.file.protection = False


    def read_file(self, file_name):
        file_node = self.tree.openFile(os.path.join(self.currentPath, file_name))
        
        # busy waiting
        while(file_node.file.protection):
            pass
        
        fileRead = open(file_node.file.path, 'r')
        return fileRead.read()


    def read_from_file(self, file_name, location, size):
        file_node = self.tree.openFile(file_name)

        # busy waiting
        while(file_node.file.protection):
            pass

        fileRead = open(file_node.file.path)
        fileRead.seek(location)
        return fileRead.read(size)


    def file_truncate(self, file_name, size):
        file_node = self.tree.openFile(file_name)

        # busy waiting
        while(file_node.file.protection):
            pass

        file_path = os.path.join(self.currentPath, file_name)
        fileTrun = open(file_path, 'a')
        fileTrun.truncate(size)
        fileTrun.close
        file_node.file.size = os.path.getsize(file_path)


    def move_file_content(self, file_name, initial_index, final_index, size):
        tempFile = open("tempFile.txt","w+")

        file_node = self.tree.openFile(file_name)
        
        # busy waiting
        while(file_node.file.protection):
            pass
        
        #apply protection and start processes
        file_node.file.protection = True
        openedFile = open(file_node.file.path, 'r+')

        tempFile.write(openedFile.read())
        openedFile.truncate(0)

        # read data to cut
        tempFile.seek(initial_index, 0)
        copied_data = tempFile.read(size)

        # move data till the copied location
        tempFile.seek(0)
        openedFile.seek(0)
        openedFile.write(tempFile.read(initial_index))

        # then continue the moving process 
        # after the copied location till the paste location
        tempFile.seek(initial_index + size)
        openedFile.write(tempFile.read(final_index))

        # paste the copied data to the openned file
        openedFile.write(copied_data)

        # # move the remaining data
        openedFile.write(tempFile.read())

        os.remove("tempFile.txt")
        tempFile.close
        openedFile.close

        #remove protection
        file_node.file.protection = False



    def moveFile(self, file_path, dir_path):
        file_node = self.tree.openFile(os.path.join(self.currentPath, file_path))

        # busy waiting
        while(file_node.file.protection):
            pass

        # disconnect node from current parent
        self.tree.preloc.children.remove(file_node)
        
        # find new parent (dir) and connect node with it
        self.tree.changeDir(dir_path)
        new_dir_node = self.tree.loc
        new_dir_node.children.append(file_node)



    def remove_file(self, file_path):
        node = self.tree.openFile(file_path)

        # busy waiting
        while(node.file.protection):
            pass

        self.tree.preloc.children.remove(node)
        # print("path recieved: ", file_path)
        os.remove(file_path)

    def make_dir(self, dir_name):
        path = os.path.join(self.currentPath, dir_name)
        newDir = Dir(os.path.basename(dir_name), path)
        self.tree.loc = self.tree.root
        self.tree.addNode(newDir)
        os.makedirs(dir_name)


    def changeDir(self, dir_path):
        if (dir_path == ".."):
            self.tree.searchFromRoot(self.currentPath)
            self.tree.root = self.tree.preloc

        else:     
            self.tree.changeDir(dir_path)
            self.tree.root = self.tree.loc
        # global self.currentPath 
        # print("path before: ", self.currentPath)
        # self.currentPath = os.path.join(self.currentPath, dir_path)
        self.currentPath = self.tree.root.dir.path
        # print("path changed: ", self.currentPath)

    def getDataStructure(self):
        return self.tree