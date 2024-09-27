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

current_dir = ""  # Путь в архиве, где находимся

def command_cd(path, archive_path):
    global current_dir
    with zipfile.ZipFile(archive_path, 'r') as zip_ref:
        if path == '..':
            if current_dir:
                current_dir = '/'.join(current_dir.rstrip('/').split('/')[:-1])
        else:
            new_path = os.path.join(current_dir, path).replace("\\", "/")
            if any(f.startswith(new_path + '/') for f in zip_ref.namelist()):
                current_dir = new_path
            else:
                console.text_list.append(f"ERROR: Directory {path} not found")

def command_ls(archive_path):
    global current_dir
    with zipfile.ZipFile(archive_path, 'r') as zip_ref:
        files_list = [f for f in zip_ref.namelist() if f.startswith(current_dir)]
        for file in files_list:
            display_name = file[len(current_dir):].strip("/")
            console.text_list.append(display_name)

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