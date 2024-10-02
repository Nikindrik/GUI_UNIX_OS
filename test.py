import unittest

from core import console
from GUI_UNIX_OS.core.emulator import Emulator, current_dir
import zipfile
import os

class TestEmulator(unittest.TestCase):

    def set_up(self):
        # Мои любимые тестики)
        self.test_archive = 'test.zip'
        with zipfile.ZipFile(self.test_archive, 'w') as zf:
            zf.writestr('systeam/dir1/file1.txt', 'Hello World\n')
            zf.writestr('systeam/dir2/file2.txt', 'Another line\n')

    def tear_down(self):
        os.remove(self.test_archive)  # Сносим эту херню всю

    def test_ls_root(self):
        emu = Emulator(self.test_archive)
        emu.read_command('ls')
        self.assertIn('dir1', console.text_list)
        self.assertIn('dir2', console.text_list)

    def test_cd_directory(self):
        emu = Emulator(self.test_archive)
        emu.read_command('cd dir1')
        self.assertEqual(current_dir, 'systeam/dir1/')

    def test_wc_file(self):
        emu = Emulator(self.test_archive)
        emu.read_command('wc file1.txt')
        self.assertIn('Lines: 1', console.text_list)
        self.assertIn('Words: 2', console.text_list)
        self.assertIn('Characters: 12', console.text_list)

    def test_mv_file(self):
        emu = Emulator(self.test_archive)
        emu.read_command('mv dir1/file1.txt dir1/file3.txt')
        self.assertIn('Moved dir1/file1.txt to dir1/file3.txt', console.text_list)

if __name__ == '__main__':
    unittest.main()