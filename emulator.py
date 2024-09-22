import console
import input_box
import os

files_list = []

def command_help():
    console.text_list.append("List of commands:")
    console.text_list.append(" help")
    console.text_list.append(" ls")
    console.text_list.append(" cd")
    console.text_list.append("    cd with .. example 'cd ..'")
    console.text_list.append("    cd with path example 'cd /path'")
    console.text_list.append(" exit")
    console.text_list.append(" wc")
    console.text_list.append(" mv")

def command_clear():
    console.text_list.clear()

def command_ls():
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

def command_cd(path):
    if path != '..':
        new_dir = os.getcwd() + path
        if os.path.isdir(new_dir):
            os.chdir(new_dir)
        else:
            console.text_list.append("ERROR with cd command")
    else:
        os.chdir('..')

def command_wc():
    pass

def command_mv():
    pass


class Emulator():
    def __init__(self):
        pass

    def read_command(self, command):
        parts = command.split(" ")
        if command == "help":
            command_help()
        elif command == "clear":
            command_clear()
        elif command == "exit":
            exit()
        elif command == "ls":
            command_ls()
        elif parts[0] == "cd" and len(parts) > 1:
            command_cd(parts[1])
        elif command == "wc":
            command_wc()
        elif command == "mv":
            command_mv()
        else:
            console.text_list.append("ERROR")
        input_box.input_history.append(command)
        input_box.history_step = 0