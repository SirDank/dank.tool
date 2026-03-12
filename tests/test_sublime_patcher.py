import unittest
from unittest.mock import patch
import os
import shutil
import tempfile
import importlib.util

# Load the module dynamically since it has dots in its name
module_name = "mrpepe.sublime-patcher"
file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "__modules__", f"{module_name}.py")

# Mock some dependencies to avoid runtime errors when loading the module
import sys
import types
sys.modules['dankware'] = types.ModuleType('dankware')
sys.modules['dankware'].align = lambda x: x
sys.modules['dankware'].clr = lambda x, colour_two=None: x
sys.modules['dankware'].cls = lambda: None
sys.modules['dankware'].cyan = 'cyan'
sys.modules['dankware'].fade = lambda x, y: x
sys.modules['dankware'].green_bright = 'green'
sys.modules['dankware'].magenta = 'magenta'
sys.modules['dankware'].white_bright = 'white'
sys.modules['dankware'].yellow_bright = 'yellow'

spec = importlib.util.spec_from_file_location(module_name, file_path)
patcher_module = importlib.util.module_from_spec(spec)

# Use patch to mock input(), print(), and Tkinter classes to prevent blocking and errors
mock_tk = patch('tkinter.Tk').start()
# Make askopenfilename return a dummy path that doesn't trigger the `.endswith("sublime_text.exe")` condition
mock_filedialog = patch('tkinter.filedialog.askopenfilename', return_value="").start()

# We need to break the infinite loop in main() by making input() raise an exception
# But we can also just let it execute main(), but how to break out of while True?
# It breaks out if patch_exe is called. We can make askopenfilename return a valid path,
# but we actually just want to prevent main from hanging or crashing.
# Let's mock patch_exe so it doesn't do anything when called during module load.
with patch('builtins.input', return_value=""), patch('builtins.print'):
    # We will temporarily replace the askopenfilename mock to return something that breaks the loop
    # actually, the while True loop only breaks when `patch_exe` is called:
    # if input_file.endswith("sublime_text.exe"):
    #     patch_exe(input_file)
    #     break
    # So we MUST return a string ending in sublime_text.exe to break the loop!
    # Let's create a temporary dummy file to satisfy os.chdir inside patch_exe.

    temp_load_dir = tempfile.mkdtemp()
    dummy_exe = os.path.join(temp_load_dir, "sublime_text.exe")
    with open(dummy_exe, "wb") as f:
        f.write(b"")

    with patch('tkinter.filedialog.askopenfilename') as mock_askopenfilename:
        # It calls replace("/", "\\") on the result, so we need to return a string
        # that supports .replace()
        class DummyString(str):
            def replace(self, *args, **kwargs):
                return self

        # Save cwd before module load because it changes cwd inside patch_exe
        original_cwd = os.getcwd()
        mock_askopenfilename.return_value = DummyString(dummy_exe)
        spec.loader.exec_module(patcher_module)
        os.chdir(original_cwd)

    shutil.rmtree(temp_load_dir)


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
        # Edge cases
        self.assertFalse(patcher_module.is_patched(None))
        self.assertFalse(patcher_module.is_patched(b""))
        self.assertFalse(patcher_module.is_patched(b"\x00\x01\x02"))

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