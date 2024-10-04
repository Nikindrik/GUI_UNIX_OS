import unittest
import os

class TestEmulator(unittest.TestCase):
    def setUp(self):
        """Инициализация тестовой среды."""
        self.archive_path = 'test_archive.zip'
        self.emulator = Emulator(self.archive_path)
        self.emulator.create_file_system()

    def tearDown(self):
        """Удаление тестовых файлов после теста."""
        if os.path.exists(self.archive_path):
            os.remove(self.archive_path)

    def test_file_system_creation(self):
        """Проверка создания файловой системы."""
        self.assertTrue(os.path.exists(self.archive_path), "Test archive was not created")

        with zipfile.ZipFile(self.archive_path, 'r') as zf:
            self.assertIn('file1.txt', zf.namelist())
            self.assertIn('dir1/file2.txt', zf.namelist())
            self.assertIn('dir1/file3.txt', zf.namelist())

    def test_ls_command(self):
        """Проверка команды ls."""
        self.emulator.read_command("ls")
        self.assertIn("file1.txt", self.emulator.console_output)
        self.assertIn("Listing directory: /", self.emulator.console_output)

if __name__ == '__main__':
    unittest.main()