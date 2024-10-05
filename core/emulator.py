import zipfile
import os
from core import console


class Emulator:
    def __init__(self, archive_path):
        self.archive_path = archive_path
        self.current_dir = "systeam/"  # Начальная директория
        self.files_list = []

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

    def command_ls(self):
        if self.current_dir == 'systeam/':
            console.text_list.append("Listing directory: /")
        else:
            console.text_list.append(f"Listing directory: {self.current_dir[7:]}")

        with zipfile.ZipFile(self.archive_path, 'r') as zip_ref:
            self.files_list = [f[len(self.current_dir):].split('/')[0]
                               for f in zip_ref.namelist()
                               if f.startswith(self.current_dir) and f != self.current_dir]
            self.files_list = sorted(set(self.files_list))
            for file in self.files_list:
                console.text_list.append(file)

    def command_cd(self, path):
        with zipfile.ZipFile(self.archive_path, 'r') as zip_ref:
            if path == '..':
                if self.current_dir != 'systeam/':
                    self.current_dir = '/'.join(self.current_dir.rstrip('/').split('/')[:-1]) + '/'
            elif path == "/":
                self.current_dir = 'systeam/'
            else:
                new_path = os.path.join(self.current_dir, path).replace("\\", "/") + '/'
                if any(f.startswith(new_path) for f in zip_ref.namelist()):
                    self.current_dir = new_path
                else:
                    console.text_list.append(f"ERROR: Directory {path} not found")

    def command_wc(self, filename):
        with zipfile.ZipFile(self.archive_path, 'r') as zip_ref:
            file_path = os.path.join(self.current_dir, filename).replace("\\", "/")
            if file_path in zip_ref.namelist():
                with zip_ref.open(file_path) as file:
                    content = file.read().decode()
                    lines = content.splitlines()
                    words = content.split()
                    chars = len(content)

                    console.text_list.append(f"Lines: {len(lines)}")
                    console.text_list.append(f"Words: {len(words)}")
                    console.text_list.append(f"Characters: {chars}")
            else:
                console.text_list.append(f"ERROR: File {filename} not found")

    def command_mv(self, source, destination):
        with zipfile.ZipFile(self.archive_path, 'a') as zip_ref:
            source_path = os.path.join(self.current_dir, source).replace("\\", "/")
            dest_path = os.path.join(self.current_dir, destination).replace("\\", "/")

            if source_path in zip_ref.namelist():
                with zip_ref.open(source_path) as src_file:
                    content = src_file.read()

                zip_ref.writestr(dest_path, content)
                # Удаляем старый файл
                with zipfile.ZipFile(self.archive_path, 'w') as zf:
                    for item in zip_ref.infolist():
                        if item.filename != source_path:
                            zf.writestr(item, zip_ref.read(item.filename))

                console.text_list.append(f"Moved {source} to {destination}")
            else:
                console.text_list.append(f"ERROR: File {source} not found")

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