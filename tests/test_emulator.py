import unittest
from core.emulator import Emulator, command_ls, command_mv, command_wc, command_clear, command_help, command_cd
from core import console


class TestEmulator(unittest.TestCase):
    def setUp(self):
        self.archive_path = 'test_sys.zip'
        self.emulator = Emulator(self.archive_path)
        console.text_list.clear()

    def test_ls_root(self):
        command_ls(self.archive_path)
        print(console.text_list)
        self.assertIn("Listing directory: /", console.text_list[0])
        self.assertIn("dir1", console.text_list[1])
        self.assertIn("so.txt", console.text_list[2])
        self.assertIn("text.txt", console.text_list[3])

        print(console.text_list)
        command_cd("dir1", self.archive_path)
        command_ls(self.archive_path)
        self.assertIn("Listing directory: /dir1/", console.text_list[0])
        self.assertIn("a.txt", console.text_list[1])


    '''def test_ls_empty_directory(self):
        command_cd('empty_dir', self.archive_path)
        command_ls(self.archive_path)
        self.assertEqual(len(console.text_list), 1)
        self.assertIn("Listing directory: empty_dir", console.text_list)'''

if __name__ == '__main__':
    unittest.main()