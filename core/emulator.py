from core import console
import zipfile
import os
from core import input_box  # Импортируем модуль input_box

files_list = []
current_dir = "systeam/"  # Начальная директория


# Вывод используемых команд
def command_help():
    console.text_list.append("List of commands:")
    console.text_list.append(" help - displays available commands and their brief descriptions")
    console.text_list.append(" ls - lists directories and files in the current working directory")
    console.text_list.append(" cd - сhanges the current directory in the virtual filesystem")
    console.text_list.append(" exit - exits the emulator or application")
    console.text_list.append(" wc - counts words, lines, or characters in a file")
    console.text_list.append(" mv - moves or renames files or directories")
    console.text_list.append(" clear - clears the console output screen")

# Отчистка консоли
def command_clear():
    console.text_list.clear()

# Команда для показа содержимого текущей директории
def command_ls(archive_path):
    global current_dir
    console.text_list.append(f"Listing directory: {current_dir}")

    with zipfile.ZipFile(archive_path, 'r') as zip_ref:
        files_list = [f[len(current_dir):].split('/')[0] for f in zip_ref.namelist() if
                      f.startswith(current_dir) and f != current_dir]
        files_list = sorted(set(files_list))  # Убираем дублирующиеся имена (директории)

        for file in files_list:
            console.text_list.append(file)


# Команда для перехода в директорию
def command_cd(path, archive_path):
    global current_dir
    with zipfile.ZipFile(archive_path, 'r') as zip_ref:
        if path == '..':
            if current_dir != 'systeam/':
                current_dir = '/'.join(current_dir.rstrip('/').split('/')[:-1]) + '/'
        else:
            new_path = os.path.join(current_dir, path).replace("\\", "/") + '/'
            if any(f.startswith(new_path) for f in zip_ref.namelist()):
                current_dir = new_path
            else:
                console.text_list.append(f"ERROR: Directory {path} not found")

# Команда mv для перемещения файлов
def command_mv(source, destination, archive_path):
    with zipfile.ZipFile(archive_path, 'a') as zip_ref:
        source_path = os.path.join(current_dir, source).replace("\\", "/")
        dest_path = os.path.join(current_dir, destination).replace("\\", "/")

        if source_path in zip_ref.namelist():
            with zip_ref.open(source_path) as src_file:
                content = src_file.read()

            zip_ref.writestr(dest_path, content)
            # Удаляем старый файл
            with zipfile.ZipFile(archive_path, 'w') as zf:
                for item in zip_ref.infolist():
                    if item.filename != source_path:
                        zf.writestr(item, zip_ref.read(item.filename))

            console.text_list.append(f"Moved {source} to {destination}")
        else:
            console.text_list.append(f"ERROR: File {source} not found")

class Emulator:
    def __init__(self, archive_path):
        self.archive_path = archive_path

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
        elif parts[0] == "wc" and len(parts) > 1:
            command_wc(parts[1], self.archive_path)
        elif parts[0] == "mv" and len(parts) > 2:
            command_mv(parts[1], parts[2], self.archive_path)
        else:
            console.text_list.append("ERROR: Invalid command")
        input_box.input_history.append(command)
        input_box.history_step = 0