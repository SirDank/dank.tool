import sys
import builtins
import unittest
from unittest.mock import patch, MagicMock
import subprocess
import os
import types

# Mock input to prevent EOFError during module execution
builtins.input = MagicMock()

# Create mock objects for the dependencies that we don't have installed
class MockDankware:
    clr = lambda *args, **kwargs: ""
    cls = lambda *args, **kwargs: ""
    err = lambda *args, **kwargs: ""
    github_file_selector = lambda *args, **kwargs: []
    green_bright = ""
    rm_line = lambda *args, **kwargs: ""

class MockRichAlign:
    center = lambda *args, **kwargs: ""

class MockRichColumns:
    pass

class MockRichConsole:
    def print(self, *args, **kwargs):
        pass

class MockRichPanel:
    pass

# Mock dependencies to allow importing without them installed
sys.modules['requests'] = MagicMock()
mock_dankware = MockDankware()
sys.modules['dankware'] = mock_dankware

sys.modules['rich'] = types.ModuleType('rich')
sys.modules['rich.align'] = types.ModuleType('rich.align')
sys.modules['rich.align'].Align = MockRichAlign
sys.modules['rich.columns'] = types.ModuleType('rich.columns')
sys.modules['rich.columns'].Columns = MockRichColumns
sys.modules['rich.console'] = types.ModuleType('rich.console')
sys.modules['rich.console'].Console = MockRichConsole
sys.modules['rich.panel'] = types.ModuleType('rich.panel')
sys.modules['rich.panel'].Panel = MockRichPanel

# Import the module dynamically since it has dots in its filename
import importlib.util

spec = importlib.util.spec_from_file_location("dank_winget", "__modules__/dank.winget.py")
dank_winget = importlib.util.module_from_spec(spec)

# Mock some functions that get executed on import
dank_winget.main = MagicMock()
dank_winget.install_winget = MagicMock()
dank_winget.winget_installed = MagicMock(return_value=True)

try:
    with patch('builtins.input', return_value=''):
        spec.loader.exec_module(dank_winget)
except Exception as e:
    print(f"Error loading module: {e}")


class TestWingetInstalled(unittest.TestCase):
    @patch('subprocess.run')
    def test_winget_installed_success(self, mock_run):
        # Setup mock to return success
        mock_process = MagicMock()
        mock_process.returncode = 0
        mock_run.return_value = mock_process

        # Execute
        result = dank_winget.winget_installed()

        # Assert
        self.assertTrue(result)
        mock_run.assert_called_once_with(
            ["winget", "--info"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True,
        )

    @patch('subprocess.run')
    def test_winget_installed_failure(self, mock_run):
        # Setup mock to return failure
        # In the original file the script called check=True, which caused subprocess.CalledProcessError
        mock_run.side_effect = subprocess.CalledProcessError(1, ["winget", "--info"])

        # Execute
        result = dank_winget.winget_installed()

        # Assert
        self.assertFalse(result)

    @patch('subprocess.run')
    def test_winget_installed_not_found(self, mock_run):
        # Setup mock to raise FileNotFoundError
        mock_run.side_effect = FileNotFoundError()

        # Execute
        result = dank_winget.winget_installed()

        # Assert
        self.assertFalse(result)


class TestDankWinget(unittest.TestCase):
    def test_cleanup_result(self):
        """Test that cleanup_result correctly formats strings in a list."""

        # Test basic stripping
        cmd = ["  hello  ", "  world  "]
        result = dank_winget.cleanup_result(cmd)
        self.assertEqual(result, ["hello", "world"])

        # Test double space replacement
        cmd = ["hello  world", "foo    bar"]
        result = dank_winget.cleanup_result(cmd)
        self.assertEqual(result, ["helloworld", "foobar"])

        # Test mixed scenario
        cmd = ["  some  text  here  "]
        result = dank_winget.cleanup_result(cmd)
        self.assertEqual(result, ["sometexthere"])

        # Test empty list
        cmd = []
        result = dank_winget.cleanup_result(cmd)
        self.assertEqual(result, [])

        # Test list with empty strings
        cmd = ["", "  ", "    "]
        result = dank_winget.cleanup_result(cmd)
        self.assertEqual(result, ["", "", ""])

if __name__ == '__main__':
    unittest.main()
