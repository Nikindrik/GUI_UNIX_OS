import unittest
import zipfile
import os
from io import BytesIO
from core import console
from core import emulator


class TestEmulator(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Создаем виртуальный zip-файл в памяти для тестов
        cls.memory_zip = BytesIO()
        with zipfile.ZipFile(cls.memory_zip, 'w') as zf:
            zf.writestr('systeam/file1.txt', 'Hello World\nThis is a test file.')
            zf.writestr('systeam/dir1/file2.txt', 'Another file in a subdirectory.')
            zf.writestr('systeam/dir1/dir2/file3.txt', 'Nested directory file.')

        # Сохраняем данные zip-файла в памяти
        cls.memory_zip.seek(0)

        # Сохраняем путь к виртуальной файловой системе
        cls.archive_path = 'test_virtual_fs.zip'

        # Записываем виртуальный zip-файл на диск для использования в тестах
        with open(cls.archive_path, 'wb') as f:
            f.write(cls.memory_zip.read())

    @classmethod
    def tearDownClass(cls):
        # Удаляем созданный архив после завершения всех тестов
        if os.path.exists(cls.archive_path):
            os.remove(cls.archive_path)

    def setUp(self):
        # Перед каждым тестом сбрасываем вывод консоли
        console.text_list = []

        # Создаем новый экземпляр эмулятора перед каждым тестом
        self.emulator = emulator(self.archive_path)

    def test_cd_root(self):
        # Проверка перехода в корневую директорию
        self.emulator.command_cd('/')
        self.assertEqual(self.emulator.current_dir, 'systeam/')
        self.assertIn('Changed directory to: /', console.text_list[-1])

    def test_cd_subdir(self):
        # Проверка перехода в поддиректорию
        self.emulator.command_cd('dir1')
        self.assertEqual(self.emulator.current_dir, 'systeam/dir1/')
        self.assertIn('Changed directory to: /dir1/', console.text_list[-1])

    def test_cd_up_directory(self):
        # Проверка перехода на уровень выше
        self.emulator.command_cd('dir1')
        self.emulator.command_cd('..')
        self.assertEqual(self.emulator.current_dir, 'systeam/')
        self.assertIn('Changed directory to: /', console.text_list[-1])

    def test_ls_root(self):
        # Проверка вывода содержимого корневой директории
        self.emulator.command_ls()
        self.assertIn('Listing directory: /', console.text_list)
        self.assertIn('file1.txt', console.text_list)
        self.assertIn('dir1', console.text_list)

    def test_ls_subdir(self):
        # Проверка вывода содержимого поддиректории
        self.emulator.command_cd('dir1')
        self.emulator.command_ls()
        self.assertIn('Listing directory: /dir1/', console.text_list)
        self.assertIn('file2.txt', console.text_list)
        self.assertIn('dir2', console.text_list)

    def test_wc(self):
        # Проверка подсчета строк, слов и символов в файле
        self.emulator.command_wc('file1.txt')
        self.assertIn('Lines: 2', console.text_list)
        self.assertIn('Words: 6', console.text_list)
        self.assertIn('Characters: 29', console.text_list)

    def test_invalid_cd(self):
        # Проверка ошибки при переходе в несуществующую директорию
        self.emulator.command_cd('nonexistent')
        self.assertIn("ERROR: Directory 'nonexistent' not found", console.text_list)

    def test_invalid_wc(self):
        # Проверка ошибки при попытке прочитать несуществующий файл
        self.emulator.command_wc('nonexistent.txt')
        self.assertIn('ERROR: File nonexistent.txt not found', console.text_list)

    def test_mv_file(self):
        # Проверка перемещения файла в новую директорию
        self.emulator.command_mv('file1.txt', 'dir1/file1_moved.txt')
        self.emulator.command_cd('dir1')
        self.emulator.command_ls()
        self.assertIn('file1_moved.txt', console.text_list)
        self.assertNotIn('file1.txt', console.text_list)


if __name__ == '__main__':
    unittest.main()