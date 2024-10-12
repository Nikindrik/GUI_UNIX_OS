import unittest
from core.emulator import Emulator
from core import console
import os
import zipfile

class TestEmulator(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Создаем тестовый ZIP-файл для эмуляции файловой системы
        cls.archive_path = 'test_archive.zip'
        with zipfile.ZipFile(cls.archive_path, 'w') as zipf:
            zipf.writestr('systeam/dir1/', '')  # Создание директории
            zipf.writestr('systeam/file3.txt', 'Another file in a subdirectory_')
            zipf.writestr('systeam/file1.txt', 'Hello World\nThis is a test file')  # Создание файла
            zipf.writestr('systeam/dir1/file2.txt', 'Another file in a subdirectory')
            zipf.writestr('systeam/dir1/file5.txt', 'Another file in a subdirectory NOT FAKE')

    def setUp(self):
        # Создаем новый экземпляр эмулятора для каждого теста и очищаем консольный вывод
        self.emulator = Emulator(self.archive_path)
        console.text_list.clear()

    @classmethod
    def tearDownClass(cls):
        # Удаление тестового ZIP-файла после завершения тестов
        os.remove(cls.archive_path)

    def test_cd_root(self):
        self.emulator.command_cd('/')
        self.assertIn("Changed directory to: /", console.text_list)

    def test_cd_subdirectory(self):
        self.emulator.command_cd('dir1')
        self.assertIn("Changed directory to: /dir1/", console.text_list)
    def test_cd_invalid_directory(self):
        self.emulator.command_cd('nonexistent')
        self.assertIn("ERROR: Directory 'nonexistent' not found", console.text_list)

    def test_ls_root_directory(self):
        self.emulator.command_ls()
        self.assertIn("Listing directory: /", console.text_list)
        self.assertIn("dir1", console.text_list)
        self.assertIn("file1.txt", console.text_list)

    def test_ls_subdirectory(self):
        self.emulator.command_cd('dir1')
        self.emulator.command_ls()
        self.assertIn("Changed directory to: /dir1/", console.text_list[0])
        self.assertIn("Listing directory: /dir1/", console.text_list[1])
        self.assertIn("file2.txt", console.text_list[2])

    def test_ls_not_a_directory(self):
        self.emulator.command_cd('file1.txt')
        self.emulator.command_ls()
        self.assertIn("ERROR: Not a directory", console.text_list)

    def test_wc_file(self):
        self.emulator.command_wc('file1.txt')
        self.assertIn("Lines: 2", console.text_list[0])
        self.assertIn("Words: 7", console.text_list[1])
        self.assertIn("Characters: 31", console.text_list[2])

    def test_wc_file_in_subdirectory(self):
        self.emulator.command_cd('dir1')
        self.emulator.command_wc('file2.txt')
        self.assertIn("Changed directory to: /dir1/", console.text_list[0])
        self.assertIn("Lines: 1", console.text_list[1])
        self.assertIn("Words: 5", console.text_list[2])
        self.assertIn("Characters: 30", console.text_list[3])

    def test_wc_nonexistent_file(self):
        self.emulator.command_wc('nonexistent.txt')
        self.assertIn("ERROR: File nonexistent.txt not found", console.text_list)

    def test_mv_file_within_directory(self):
        self.emulator.command_mv('file3.txt', 'file3_moved.txt')
        self.assertIn("Moved file3.txt to file3_moved.txt", console.text_list)
    def test_mv_file_in_subdirectory(self):
        self.emulator.command_cd('dir1')
        self.emulator.command_mv('file5.txt', 'file5_moved.txt')
        self.assertIn("Moved file5.txt to file5_moved.txt", console.text_list)

    def test_mv_nonexistent_file(self):
        self.emulator.command_mv('nonexistent.txt', 'file3.txt')
        self.assertIn("ERROR: File nonexistent.txt not found", console.text_list)

    def test_help_command(self):
        self.emulator.command_help()
        expected_help = [
            'List of commands:',
            ' help - displays available commands and their brief descriptions',
            ' ls - lists directories and files in the current working directory',
            ' cd - changes the current directory in the virtual filesystem', ' exit - exits the emulator or application',
            ' wc - counts words, lines, or characters in a file',
            ' mv - moves or renames files or directories',
            ' clear - clears the console output screen'
        ]
        for i in range(7):
            self.assertIn(expected_help[i], console.text_list[i])

    def test_clear_command(self):
        console.text_list.append("Some output")
        self.emulator.command_clear()
        self.assertEqual(len(console.text_list), 0)

if __name__ == '__main__':
    unittest.main()