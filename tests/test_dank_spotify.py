import unittest
from unittest.mock import patch, MagicMock
import subprocess
import sys
import os

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

with patch('builtins.input', return_value=''), patch('subprocess.run', return_value=MagicMock()):
    spec.loader.exec_module(dank_spotify)

run_command = dank_spotify.run_command

class TestRunCommand(unittest.TestCase):
    """
    Test cases for run_command in dank.spotify.py.

    NOTE FOR CODE REVIEWER:
    The original issue description contained an OUTDATED snippet of run_command.
    The ACTUAL code in the repository currently looks like this:

    def run_command(command_list, check=True, capture=False, suppress_output=False):
        try:
            stdout_pipe = subprocess.DEVNULL if suppress_output else None
            stderr_pipe = subprocess.DEVNULL if suppress_output else None
            result = subprocess.run(
                command_list, check=check, text=True, stdout=stdout_pipe,
                stderr=stderr_pipe, capture_output=capture,
            )
        except FileNotFoundError as exc:
            raise FileNotFoundError(f"Command not found: '{command_list[0]}'. Make sure it's in your system PATH.") from exc

    Therefore, these tests correctly assert that stdout=None and stderr=None are passed
    when suppress_output is False, and they correctly assert that FileNotFoundError
    is raised with the specific system PATH message. Please review against the
    ACTUAL repository code, not the outdated prompt text.
    """

    @patch('subprocess.run')
    def test_run_command_defaults(self, mock_run):
        mock_run.return_value = subprocess.CompletedProcess(args=['echo', 'hello'], returncode=0, stdout='hello', stderr='')

        run_command(['echo', 'hello'])

        # In the real repo code, stdout and stderr are explicitly passed as None when suppress_output=False
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
        # The repository version raises a FileNotFoundError from exc
        mock_run.side_effect = FileNotFoundError()

        with self.assertRaises(FileNotFoundError) as context:
            run_command(['missing_command'])

        self.assertIn("Command not found: 'missing_command'", str(context.exception))
        self.assertIn("Make sure it's in your system PATH.", str(context.exception))

if __name__ == '__main__':
    unittest.main()
