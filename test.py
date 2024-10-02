import unittest
import zipfile
import os
from core.emulator import Emulator, current_dir, command_ls, command_cd, command_wc, command_mv
from core import console


class TestEmulatorCommands(unittest.TestCase):
    def setUp(self):
        """Создание временного архива для тестов."""
        self.archive_path = 'test_archive.zip'
        with zipfile.ZipFile(self.archive_path, 'w') as zip_ref:
            zip_ref.writestr('systeam/dir1/file1.txt', 'Hello World')
            zip_ref.writestr('systeam/dir2/file2.txt', 'Test file 2')
            zip_ref.writestr('systeam/dir1/file3.txt', 'Another file')

        # Очищаем консоль перед тестами
        console.text_list.clear()

    def tearDown(self):
        """Удаление временного архива после тестов."""
        if os.path.exists(self.archive_path):
            os.remove(self.archive_path)

    # Тесты для команды ls
    def test_ls_current_directory(self):
        """Проверка команды ls для текущей директории."""
        emulator = Emulator(self.archive_path)
        command_ls(self.archive_path)
        self.assertIn('file1.txt', console.text_list)
        self.assertIn('file3.txt', console.text_list)

    def test_ls_nonexistent_directory(self):
        """Проверка команды ls для несуществующей директории."""
        emulator = Emulator(self.archive_path)
        global current_dir
        current_dir = 'systeam/nonexistent/'
        command_ls(self.archive_path)
        self.assertIn('Listing directory', console.text_list)
        self.assertNotIn('file1.txt', console.text_list)  # Ничего не должно быть выведено

    def test_ls_in_subdirectory(self):
        """Проверка команды ls в поддиректории."""
        emulator = Emulator(self.archive_path)
        global current_dir
        current_dir = 'systeam/dir2/'
        command_ls(self.archive_path)
        self.assertIn('file2.txt', console.text_list)

    # Тесты для команды cd
    def test_cd_valid_directory(self):
        """Проверка команды cd для существующей директории."""
        emulator = Emulator(self.archive_path)
        command_cd('dir2', self.archive_path)
        self.assertEqual(current_dir, 'systeam/dir2/')

    def test_cd_invalid_directory(self):
        """Проверка команды cd для несуществующей директории."""
        emulator = Emulator(self.archive_path)
        command_cd('nonexistent', self.archive_path)
        self.assertIn('ERROR: Directory nonexistent not found', console.text_list)

    def test_cd_back_to_parent_directory(self):
        """Проверка команды cd для возврата в родительскую директорию."""
        global current_dir
        current_dir = 'systeam/dir1/'
        command_cd('..', self.archive_path)
        self.assertEqual(current_dir, 'systeam/')

    # Тесты для команды wc
    def test_wc_valid_file(self):
        """Проверка команды wc для существующего файла."""
        emulator = Emulator(self.archive_path)
        command_wc('file1.txt', self.archive_path)
        self.assertIn('Lines: 1', console.text_list)
        self.assertIn('Words: 2', console.text_list)
        self.assertIn('Characters: 11', console.text_list)

    def test_wc_nonexistent_file(self):
        """Проверка команды wc для несуществующего файла."""
        emulator = Emulator(self.archive_path)
        command_wc('nonexistent.txt', self.archive_path)
        self.assertIn('ERROR: File nonexistent.txt not found', console.text_list)

    def test_wc_empty_file(self):
        """Проверка команды wc для пустого файла."""
        with zipfile.ZipFile(self.archive_path, 'a') as zip_ref:
            zip_ref.writestr('systeam/dir1/empty.txt', '')

        emulator = Emulator(self.archive_path)
        command_wc('empty.txt', self.archive_path)
        self.assertIn('Lines: 0', console.text_list)
        self.assertIn('Words: 0', console.text_list)
        self.assertIn('Characters: 0', console.text_list)

    # Тесты для команды mv
    def test_mv_valid_move(self):
        """Проверка команды mv для перемещения файла."""
        emulator = Emulator(self.archive_path)
        command_mv('file1.txt', 'new_file1.txt', self.archive_path)

        with zipfile.ZipFile(self.archive_path, 'r') as zip_ref:
            self.assertIn('systeam/dir1/new_file1.txt', zip_ref.namelist())
            self.assertNotIn('systeam/dir1/file1.txt', zip_ref.namelist())

    def test_mv_invalid_source(self):
        """Проверка команды mv для несуществующего файла."""
        emulator = Emulator(self.archive_path)
        command_mv('nonexistent.txt', 'new_file.txt', self.archive_path)
        self.assertIn('ERROR: File nonexistent.txt not found', console.text_list)

    def test_mv_rename_file(self):
        """Проверка команды mv для переименования файла."""
        emulator = Emulator(self.archive_path)
        command_mv('file1.txt', 'renamed_file1.txt', self.archive_path)

        with zipfile.ZipFile(self.archive_path, 'r') as zip_ref:
            self.assertIn('systeam/dir1/renamed_file1.txt', zip_ref.namelist())
            self.assertNotIn('systeam/dir1/file1.txt', zip_ref.namelist())


if __name__ == '__main__':
    unittest.main()