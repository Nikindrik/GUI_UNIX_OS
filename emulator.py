import pygame
import console
import main
import input_box
import os

files_list=[]

class Emulator():
    def __init__(self):
        pass

    def read_command(self, command):
        if command == "help":
            console.text_list.append("List of commands:")
            console.text_list.append(" help")
            console.text_list.append(" ls")
            console.text_list.append(" cd")
            console.text_list.append(" exit")
            console.text_list.append(" wc")
            console.text_list.append(" mv")
        elif command == "clear":
            console.text_list.clear()
        elif command == "exit":
            exit()
        elif command == "ls":
            files_list.clear()
            items = os.listdir('.')
            for item in items:
                path = os.path.join('.', item)
                if os.path.isfile(path):
                    files_list.append(path)
                elif os.path.isdir(path):
                    files_list.append(path)
            for i in range(len(files_list)):
                console.text_list.append(files_list[i])
        elif command == "help":
            pass
        elif command == "cd":
            pass
        elif command == "wc":
            pass
        elif command == "mv":
            pass
        else:
            console.text_list.append("error")
        input_box.input_history.append(command)
        input_box.history_step = 0