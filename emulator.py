import console
import zipfile
import os
import input_box  # Импортируем модуль input_box

files_list = []
current_dir = ""

def command_help():
    console.text_list.append("List of commands:")
    console.text_list.append(" help")
    console.text_list.append(" ls")
    console.text_list.append(" cd")
    console.text_list.append(" exit")
    console.text_list.append(" wc")
    console.text_list.append(" mv")

def command_clear():
    console.text_list.clear()

def command_ls(archive_path):
    global files_list
    files_list.clear()
    with zipfile.ZipFile(archive_path, 'r') as zip_ref:
        for file in zip_ref.namelist():
            if file.startswith(current_dir):
                files_list.append(file)
    for file in files_list:
        console.text_list.append(file)

def command_cd(path, archive_path):
    global current_dir
    if path == '..':
        if '/' in current_dir:
            current_dir = '/'.join(current_dir.split('/')[:-1])
    elif path:
        new_path = os.path.join(current_dir, path)
        with zipfile.ZipFile(archive_path, 'r') as zip_ref:
            if any(f.startswith(new_path + '/') for f in zip_ref.namelist()):
                current_dir = new_path

def command_wc():
    pass

def command_mv():
    pass

class Emulator:
    def __init__(self, archive_path):
        self.archive_path = archive_path # archive_path

    def read_command(self, command):
        parts = command.split(" ")
        if command == "help":
            command_help()
        elif command == "clear":
            command_clear()
        elif command == "exit":
            exit()
        elif command == "ls":
            command_ls(self.archive_path)
        elif parts[0] == "cd" and len(parts) > 1:
            command_cd(parts[1], self.archive_path)
        elif command == "wc":
            command_wc()
        elif command == "mv":
            command_mv()
        else:
            console.text_list.append("ERROR")
        input_box.input_history.append(command)  # Используем input_box
        input_box.history_step = 0