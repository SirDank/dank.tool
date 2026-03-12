import sys
import builtins
import unittest
from unittest.mock import patch, MagicMock
import subprocess
import os
import types
import importlib.util

# Mock input to prevent EOFError during module execution
builtins.input = MagicMock()

# Mock dependencies to allow importing without them installed
sys.modules['requests'] = MagicMock()
sys.modules['dankware'] = MagicMock()
sys.modules['rich'] = MagicMock()
sys.modules['rich.align'] = MagicMock()
sys.modules['rich.columns'] = MagicMock()
sys.modules['rich.console'] = MagicMock()
sys.modules['rich.panel'] = MagicMock()

# Import the module dynamically since it has dots in its filename
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
