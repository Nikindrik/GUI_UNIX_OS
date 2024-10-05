import unittest
from core.emulator import Emulator
from core import console

class TestEmulator(unittest.TestCase):

    def setUp(self):
        self.archive_path = 'test_sys.zip'
        self.emulator = Emulator(self.archive_path)
        console.text_list.clear()

    def test_ls_root(self):
        self.emulator.command_ls()
        self.assertIn("Listing directory: /", console.text_list[0])
        self.assertIn("dir1", console.text_list[1])
        self.assertIn("so.txt", console.text_list[2])
        self.assertIn("code", console.text_list[3])

    def test_ls_dir1(self):
        self.emulator.command_cd('dir1')
        self.emulator.command_ls()
        self.assertIn("Listing directory: dir1", console.text_list)
        self.assertIn("a.txt", console.text_list)

    def test_ls_empty_directory(self):
        self.emulator.command_cd('empty_dir')
        self.emulator.command_ls()
        self.assertEqual(len(console.text_list), 1)  # Список пуст
        self.assertIn("Listing directory: empty_dir", console.text_list)

if __name__ == '__main__':
    unittest.main()