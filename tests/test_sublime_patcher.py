import unittest
from unittest.mock import patch
import os
import shutil
import tempfile
import importlib.util

# Load the module dynamically since it has dots in its name
module_name = "mrpepe.sublime-patcher"
file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "__modules__", f"{module_name}.py")

spec = importlib.util.spec_from_file_location(module_name, file_path)
patcher_module = importlib.util.module_from_spec(spec)

# Use patch to mock input() and print() during module execution to prevent blocking and noise
with patch('builtins.input', return_value=""), patch('builtins.print'):
    spec.loader.exec_module(patcher_module)


class TestSublimePatcher(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory
        self.test_dir = tempfile.mkdtemp()
        self.exe_path = os.path.join(self.test_dir, "sublime_text.exe")

        # Create a dummy executable with some data
        # Ensure it's large enough to cover the max offset in offsets_and_values (0x001C6CFB)
        self.dummy_data = bytearray([0] * (0x001C6CFB + 10))
        with open(self.exe_path, "wb") as f:
            f.write(self.dummy_data)

        # Store original cwd to restore later
        self.original_cwd = os.getcwd()

    def tearDown(self):
        # Restore cwd and remove temp directory
        os.chdir(self.original_cwd)
        shutil.rmtree(self.test_dir)

    def test_is_patched(self):
        # Not patched initially
        self.assertFalse(patcher_module.is_patched(self.dummy_data))

        # Patch the data manually
        patched_data = bytearray(self.dummy_data)
        for offset, value in patcher_module.offsets_and_values.items():
            if offset < len(patched_data):
                patched_data[offset] = value

        # Now it should be patched
        self.assertTrue(patcher_module.is_patched(patched_data))

    @patch('builtins.input', return_value="")
    @patch('builtins.print')
    def test_patch_exe(self, mock_print, mock_input):
        # Verify the file is not patched initially
        with open(self.exe_path, "rb") as f:
            data = f.read()
        self.assertFalse(patcher_module.is_patched(data))

        # Patch the executable
        patcher_module.patch_exe(self.exe_path)

        # Verify it created a backup
        backup_path = os.path.join(self.test_dir, "sublime_text.exe.bak")
        self.assertTrue(os.path.isfile(backup_path))

        # Verify the new executable is patched
        with open(self.exe_path, "rb") as f:
            data = f.read()
        self.assertTrue(patcher_module.is_patched(data))

if __name__ == "__main__":
    unittest.main()
