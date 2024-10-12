import zipfile
from zipfile import BadZipFile
import os
from core import console


class Emulator:
    def __init__(self, archive_path):
        self.archive_path = archive_path
        self.current_dir = "systeam/"
        self.files_list = []
        self.file_structure = {}
        self.open_zip_sys()

    def open_zip_sys(self):
        try:
            with zipfile.ZipFile(self.archive_path, 'r') as zip_ref:
                for file in zip_ref.namelist():
                    if file.startswith('systeam/'):
                        parts = file.split('/')[1:]  # Игнорируем корневую папку 'systeam'
                        d = self.file_structure
                        for part in parts[:-1]:
                            d = d.setdefault(part, {})
                        if parts[-1]:
                            d[parts[-1]] = None  # Отмечаем как файл
        except BadZipFile:
            console.text_list.append(f"Файл {self.archive_path} не является корректным zip-архивом.")

    def command_cd(self, path):
        target_dir = ""
        if path == '/':
            target_dir = "systeam/"
        elif path == '..':
            if self.current_dir != 'systeam/':
                target_dir = '/'.join(self.current_dir.rstrip('/').split('/')[:-1]) + '/'
            else:
                target_dir = self.current_dir
        else:
            target_dir = os.path.join(self.current_dir, path).replace("\\", "/")
            if not target_dir.endswith('/'):
                target_dir += '/'

        # Существование дриктории
        path_parts = target_dir.split('/')[1:]
        d = self.file_structure
        for part in path_parts:
            if part:
                if part in d:
                    d = d[part]
                else:
                    console.text_list.append(f"ERROR: Directory '{path}' not found")
                    return
        self.current_dir = target_dir
        console.text_list.append(f"Changed directory to: /{self.current_dir[8:]}")

    def command_ls(self):
        path_parts = self.current_dir.split('/')[1:]
        d = self.file_structure
        for part in path_parts:
            if part:
                d = d.get(part, {})

        if isinstance(d, dict):
            console.text_list.append(f"Listing directory: /{self.current_dir[8:]}")
            self.files_list = sorted(d.keys())
            for file in self.files_list:
                console.text_list.append(file)
        else:
            console.text_list.append("ERROR: Not a directory")

    def command_help(self):
        console.text_list.append("List of commands:")
        console.text_list.append(" help - displays available commands and their brief descriptions")
        console.text_list.append(" ls - lists directories and files in the current working directory")
        console.text_list.append(" cd - changes the current directory in the virtual filesystem")
        console.text_list.append(" exit - exits the emulator or application")
        console.text_list.append(" wc - counts words, lines, or characters in a file")
        console.text_list.append(" mv - moves or renames files or directories")
        console.text_list.append(" clear - clears the console output screen")

    def command_clear(self):
        console.text_list.clear()

    def read_command(self, command):
        parts = command.split(" ")
        if command == "help":
            self.command_help()
        elif command == "clear":
            self.command_clear()
        elif command == "exit":
            exit()
        elif command == "ls":
            self.command_ls()
        elif parts[0] == "cd" and len(parts) > 1:
            self.command_cd(parts[1])
        elif parts[0] == "wc" and len(parts) > 1:
            self.command_wc(parts[1])
        elif parts[0] == "mv" and len(parts) > 2:
            self.command_mv(parts[1], parts[2])
        else:
            console.text_list.append("ERROR: Invalid command")

    def command_wc(self, filename):
        try:
            with zipfile.ZipFile(self.archive_path, 'r') as zip_ref:
                file_path = os.path.join(self.current_dir, filename).replace("\\", "/")
                if file_path not in zip_ref.namelist():
                    console.text_list.append(f"ERROR: File {filename} not found")
                    return
                with zip_ref.open(file_path) as file:
                    content = file.read().decode()
                    lines = content.splitlines()
                    words = content.split()
                    chars = len(content)

                    console.text_list.append(f"Lines: {len(lines)}")
                    console.text_list.append(f"Words: {len(words)}")
                    console.text_list.append(f"Characters: {chars}")
        except BadZipFile:
            console.text_list.append(f"Файл {self.archive_path} не является корректным zip-архивом.")

    def command_mv(self, source, destination):
        try:
            source_path = os.path.join(self.current_dir, source).replace("\\", "/")
            dest_path = os.path.join(self.current_dir, destination).replace("\\", "/")
            with zipfile.ZipFile(self.archive_path, 'r') as zip_ref:
                if source_path not in zip_ref.namelist():
                    console.text_list.append(f"ERROR: File {source} not found")
                    return
                # Исходник
                content = zip_ref.read(source_path)
            # tmp архивчик
            temp_zip_path = self.archive_path + '.temp'

            with zipfile.ZipFile(self.archive_path, 'r') as zip_ref, zipfile.ZipFile(temp_zip_path, 'w') as temp_zip:
                for item in zip_ref.infolist():
                    # В tmp файл
                    if item.filename != source_path:
                        temp_zip.writestr(item, zip_ref.read(item.filename))
                temp_zip.writestr(dest_path, content)
            # Замена оригинальным временным
            os.replace(temp_zip_path, self.archive_path)
            console.text_list.append(f"Moved {source} to {destination}")

        except BadZipFile:
            console.text_list.append(f"File {self.archive_path} is not correct zip.")