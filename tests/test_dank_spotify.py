import unittest
from unittest.mock import patch, MagicMock
import subprocess
import sys
import os
import builtins

# Create a mock for dankware clr function
def mock_clr(text, color=None):
    return text

# Mock missing dependencies
sys.modules['dankware'] = MagicMock()
sys.modules['dankware'].clr = mock_clr
sys.modules['dankware'].cls = MagicMock()
sys.modules['rich'] = MagicMock()
sys.modules['rich.align'] = MagicMock()
sys.modules['rich.console'] = MagicMock()
sys.modules['translatepy'] = MagicMock()

import importlib.util

filepath = os.path.join(os.path.dirname(__file__), '..', '__modules__', 'dank.spotify.py')
spec = importlib.util.spec_from_file_location("dank.spotify", filepath)
dank_spotify = importlib.util.module_from_spec(spec)
sys.modules["dank.spotify"] = dank_spotify

with patch('builtins.input', return_value=''), patch('sys.exit'):
    try:
        spec.loader.exec_module(dank_spotify)
    except Exception:
        pass

run_command = dank_spotify.run_command

class TestRunCommand(unittest.TestCase):
    """
    Test cases for run_command in dank.spotify.py.
    """

    @patch('subprocess.run')
    def test_run_command_defaults(self, mock_run):
        mock_run.return_value = subprocess.CompletedProcess(args=['echo', 'hello'], returncode=0, stdout='hello', stderr='')

        run_command(['echo', 'hello'])

        mock_run.assert_called_once_with(
            ['echo', 'hello'],
            check=True,
            text=True,
            stdout=None,
            stderr=None,
            capture_output=False
        )

    @patch('subprocess.run')
    def test_run_command_suppress_output(self, mock_run):
        run_command(['echo', 'hello'], suppress_output=True)

        mock_run.assert_called_once_with(
            ['echo', 'hello'],
            check=True,
            text=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            capture_output=False
        )

    @patch('subprocess.run')
    def test_run_command_capture(self, mock_run):
        run_command(['echo', 'hello'], capture=True)

        mock_run.assert_called_once_with(
            ['echo', 'hello'],
            check=True,
            text=True,
            stdout=None,
            stderr=None,
            capture_output=True
        )

    @patch('subprocess.run')
    def test_run_command_suppress_and_capture(self, mock_run):
        run_command(['echo', 'hello'], suppress_output=True, capture=True)

        mock_run.assert_called_once_with(
            ['echo', 'hello'],
            check=True,
            text=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            capture_output=True
        )

    @patch('subprocess.run')
    def test_run_command_file_not_found(self, mock_run):
        mock_run.side_effect = FileNotFoundError()

        with self.assertRaises(FileNotFoundError) as context:
            run_command(['missing_command'])

        self.assertIn("Command not found: 'missing_command'", str(context.exception))
        self.assertIn("Make sure it's in your system PATH.", str(context.exception))

if __name__ == '__main__':
    unittest.main()
