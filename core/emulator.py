import zipfile
from zipfile import BadZipFile
import os
from core import console


class Emulator:
    def __init__(self, archive_path):
        self.archive_path = archive_path
        self.current_dir = "systeam/"  # Устанавливаем начальную директорию как "systeam"
        self.files_list = []
        self.file_structure = {}  # Словарь для хранения структуры файловой системы
        self.open_zip_sys()  # Инициализация файловой системы при создании объекта

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
            # Переход в корневую директорию
            target_dir = "systeam/"
        elif path == '..':
            # Переход на уровень выше, если это не корневая директория
            if self.current_dir != 'systeam/':
                target_dir = '/'.join(self.current_dir.rstrip('/').split('/')[:-1]) + '/'
            else:
                target_dir = self.current_dir
        else:
            # Переход в поддиректорию внутри текущей директории
            target_dir = os.path.join(self.current_dir, path).replace("\\", "/")

            # Проверяем, что целевая директория не заканчивается на '/'
            if not target_dir.endswith('/'):
                target_dir += '/'

        # Проверяем, существует ли целевая директория в структуре файловой системы
        path_parts = target_dir.split('/')[1:]  # Игнорируем 'systeam' в начале пути
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
        path_parts = self.current_dir.split('/')[1:]  # Пропускаем 'systeam' в начале
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
        except BadZipFile:
            console.text_list.append(f"Файл {self.archive_path} не является корректным zip-архивом.")

    def command_mv(self, source, destination):
        try:
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
        except BadZipFile:
            console.text_list.append(f"Файл {self.archive_path} не является корректным zip-архивом.")