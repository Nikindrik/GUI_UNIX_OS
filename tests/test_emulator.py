import unittest
import zipfile
import os
from core import emulator


class TestEmulator(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Create a temporary zip file for testing
        cls.test_zip_path = 'test_fs.zip'
        with zipfile.ZipFile(cls.test_zip_path, 'w') as zf:
            zf.writestr('systeam/text.txt', 'This is a test file.\nIt has several lines.\nAnd some words.')
            zf.writestr('systeam/dir1/a.txt', 'Another test file in a subdirectory.')

    @classmethod
    def tearDownClass(cls):
        os.remove(cls.test_zip_path)

    def setUp(self):
        self.emulator = emulator.Emulator(self.test_zip_path)

    def test_ls(self):
        # Test listing files in the root directory
        self.emulator.read_command('ls')
        self.assertIn('dir1', emulator.console.text_list)
        self.assertIn('text.txt', emulator.console.text_list)

    def test_cd(self):
        # Test changing directory to 'dir1'
        self.emulator.read_command('cd dir1')
        self.assertEqual(emulator.current_dir, 'systeam/dir1/')

        # Test changing back to root
        self.emulator.read_command('cd ..')
        self.assertEqual(emulator.current_dir, 'systeam/')

        # Test invalid directory change
        self.emulator.read_command('cd non_existent_dir')
        self.assertIn('ERROR: Directory non_existent_dir not found', emulator.console.text_list)

    def test_wc(self):
        # Test word, line, and character count for 'text.txt'
        self.emulator.read_command('wc text.txt')
        self.assertIn('Lines: 3', emulator.console.text_list)
        self.assertIn('Words: 12', emulator.console.text_list)
        self.assertIn('Characters: 45', emulator.console.text_list)

        # Test word count for non-existent file
        self.emulator.read_command('wc nonexistent.txt')
        self.assertIn('ERROR: File nonexistent.txt not found', emulator.console.text_list)

    def test_mv(self):
        # Test moving 'text.txt' to 'dir1'
        self.emulator.read_command('mv text.txt dir1/text_moved.txt')
        self.assertIn('Moved text.txt to dir1/text_moved.txt', emulator.console.text_list)

        # Test if the moved file exists in the new location
        self.emulator.read_command('ls dir1')
        self.assertIn('text_moved.txt', emulator.console.text_list)

        # Test if the original file is removed
        self.emulator.read_command('ls')
        self.assertNotIn('text.txt', emulator.console.text_list)

        # Test invalid move
        self.emulator.read_command('mv nonexistent.txt dir1/')
        self.assertIn('ERROR: File nonexistent.txt not found', emulator.console.text_list)


if __name__ == '__main__':
    unittest.main()
