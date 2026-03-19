import sys
import builtins
import unittest
from unittest.mock import MagicMock, patch
import importlib.util
import os

# Mock dependencies to allow importing without them installed
sys.modules['requests'] = MagicMock()
sys.modules['dankware'] = MagicMock()
sys.modules['dankware'].clr = lambda text, color=None: text
sys.modules['dankware'].cls = MagicMock()
sys.modules['rich'] = MagicMock()
sys.modules['rich.align'] = MagicMock()
sys.modules['rich.columns'] = MagicMock()
sys.modules['rich.console'] = MagicMock()
sys.modules['rich.panel'] = MagicMock()
sys.modules['psutil'] = MagicMock()
sys.modules['translatepy'] = MagicMock()
sys.modules['mcstatus'] = MagicMock()
sys.modules['numpy'] = MagicMock()
sys.modules['dateutil'] = MagicMock()
sys.modules['dateutil.tz'] = MagicMock()

# Import the module dynamically since it has dots in its filename
filepath = os.path.join(os.path.dirname(__file__), '..', '__src__', 'dank.tool.py')
spec = importlib.util.spec_from_file_location("dank_tool", filepath)
dank_tool = importlib.util.module_from_spec(spec)
sys.modules["dank.tool"] = dank_tool

# Mock functions that might be executed unconditionally (e.g., input, print, sys.exit)
# to avoid blocking/crashing the test runner during import
builtins.input = MagicMock()
builtins.print = MagicMock()

dank_tool._translate = lambda x: x

try:
    spec.loader.exec_module(dank_tool)
except Exception as e:
    print(f"Error loading module: {e}")
    pass

# Set some variables that are checked by dank_tool functions
dank_tool.DANK_TOOL_LANG = None
dank_tool.ONLINE_MODE = False
dank_tool.red = ""

class TestDankClearCache(unittest.TestCase):
    @patch('builtins.input')
    @patch('builtins.print')
    @patch('os.system')
    @patch('os.chdir')
    @patch('os.listdir')
    @patch('os.remove')
    @patch('os.path.expandvars', return_value='/mock/AppData/Local/Microsoft/Windows/Explorer')
    @patch('os.path.dirname', return_value='/mock/dirname')
    def test_clear_icon_cache(self, mock_dirname, mock_expandvars, mock_remove, mock_listdir, mock_chdir, mock_system, mock_print, mock_input):
        mock_input.side_effect = ['1', '0']
        mock_listdir.return_value = ['iconcache_1.db', 'thumbcache_1.db', 'iconcache_2.db']

        dank_tool.dank_clear_cache()

        # Check system commands
        mock_system.assert_any_call("taskkill /f /im explorer.exe >nul 2>&1")
        mock_system.assert_any_call(r"attrib -h iconcache*")
        mock_system.assert_any_call("start explorer.exe")

        # Check removes
        mock_remove.assert_any_call('iconcache_1.db')
        mock_remove.assert_any_call('iconcache_2.db')

        # Verify thumbcache wasn't removed
        with self.assertRaises(AssertionError):
            mock_remove.assert_any_call('thumbcache_1.db')

    @patch('builtins.input')
    @patch('builtins.print')
    @patch('os.system')
    @patch('os.chdir')
    @patch('os.listdir')
    @patch('os.remove')
    @patch('os.path.expandvars', return_value='/mock/AppData/Local/Microsoft/Windows/Explorer')
    @patch('os.path.dirname', return_value='/mock/dirname')
    def test_clear_thumbnail_cache(self, mock_dirname, mock_expandvars, mock_remove, mock_listdir, mock_chdir, mock_system, mock_print, mock_input):
        mock_input.side_effect = ['2', '0']
        mock_listdir.return_value = ['iconcache_1.db', 'thumbcache_1.db', 'thumbcache_2.db']

        dank_tool.dank_clear_cache()

        # Check system commands
        mock_system.assert_any_call("taskkill /f /im explorer.exe >nul 2>&1")
        mock_system.assert_any_call(r"attrib -h thumbcache*")
        mock_system.assert_any_call("start explorer.exe")

        # Check removes
        mock_remove.assert_any_call('thumbcache_1.db')
        mock_remove.assert_any_call('thumbcache_2.db')

    @patch('builtins.input')
    @patch('builtins.print')
    @patch('os.system')
    @patch('os.chdir')
    @patch('os.path.expandvars', return_value='/mock/AppData')
    @patch('os.path.dirname', return_value='/mock/dirname')
    def test_clear_nvidia_cache(self, mock_dirname, mock_expandvars, mock_chdir, mock_system, mock_print, mock_input):
        mock_input.side_effect = ['3', '0']

        dank_tool.dank_clear_cache()

        mock_system.assert_any_call("taskkill /f /im explorer.exe >nul 2>&1")
        mock_system.assert_any_call(r"del /f /s /q %localappdata%\NVIDIA\DXCache\*")
        mock_system.assert_any_call(r"del /f /s /q %localappdata%\NVIDIA\GLCache\*")
        mock_system.assert_any_call("start explorer.exe")

    @patch('builtins.input')
    @patch('builtins.print')
    @patch('os.system')
    @patch('os.chdir')
    @patch('os.listdir')
    @patch('os.remove')
    @patch('os.path.expandvars', return_value='/mock/AppData/Local/Microsoft/Windows/Explorer')
    @patch('os.path.dirname', return_value='/mock/dirname')
    def test_run_all_tasks(self, mock_dirname, mock_expandvars, mock_remove, mock_listdir, mock_chdir, mock_system, mock_print, mock_input):
        mock_input.side_effect = ['4', '0']
        mock_listdir.return_value = ['iconcache_1.db', 'thumbcache_1.db', 'other_file.txt']

        dank_tool.dank_clear_cache()

        mock_system.assert_any_call("taskkill /f /im explorer.exe >nul 2>&1")
        mock_system.assert_any_call(r"attrib -h iconcache*")
        mock_system.assert_any_call(r"attrib -h thumbcache*")
        mock_system.assert_any_call(r"del /f /s /q %localappdata%\NVIDIA\DXCache\*")
        mock_system.assert_any_call(r"del /f /s /q %localappdata%\NVIDIA\GLCache\*")
        mock_system.assert_any_call("start explorer.exe")

        mock_remove.assert_any_call('iconcache_1.db')
        mock_remove.assert_any_call('thumbcache_1.db')

    @patch('builtins.input')
    @patch('builtins.print')
    @patch('os.system')
    def test_invalid_choice_then_exit(self, mock_system, mock_print, mock_input):
        # Invalid input shouldn't break the loop, '0' exits
        mock_input.side_effect = ['5', 'invalid', '0']

        # In actual code, `rm_line` is called when input is invalid.
        dank_tool.rm_line = MagicMock()

        dank_tool.dank_clear_cache()

        mock_system.assert_not_called()
        self.assertEqual(dank_tool.rm_line.call_count, 2)

    @patch('builtins.input')
    @patch('builtins.print')
    @patch('os.system')
    @patch('os.chdir')
    @patch('os.listdir')
    @patch('os.remove')
    @patch('os.path.expandvars', return_value='/mock/AppData/Local/Microsoft/Windows/Explorer')
    @patch('os.path.dirname', return_value='/mock/dirname')
    def test_remove_failure(self, mock_dirname, mock_expandvars, mock_remove, mock_listdir, mock_chdir, mock_system, mock_print, mock_input):
        mock_input.side_effect = ['1', '0']
        mock_listdir.return_value = ['iconcache_error.db']
        mock_remove.side_effect = Exception("Permission denied")

        # Ensure that failure to remove doesn't crash the program
        dank_tool.dank_clear_cache()

        mock_remove.assert_called_once_with('iconcache_error.db')

if __name__ == '__main__':
    unittest.main()
