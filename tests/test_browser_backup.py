import sys
import unittest
from unittest.mock import MagicMock, patch
import importlib.util
import subprocess

# Mock necessary missing modules for Linux testing environment
sys.modules['winreg'] = MagicMock()
sys.modules['dankware'] = MagicMock()
sys.modules['psutil'] = MagicMock()
sys.modules['rich'] = MagicMock()
sys.modules['rich.align'] = MagicMock()
sys.modules['rich.console'] = MagicMock()
sys.modules['rich.live'] = MagicMock()
sys.modules['rich.panel'] = MagicMock()
sys.modules['rich.progress'] = MagicMock()
sys.modules['rich.table'] = MagicMock()
sys.modules['translatepy'] = MagicMock()

# Import the module
import importlib.machinery

spec = importlib.util.spec_from_file_location("dank_browser_backup", "__modules__/dank.browser-backup.py")
dank_browser_backup = importlib.util.module_from_spec(spec)
sys.modules["dank_browser_backup"] = dank_browser_backup
spec.loader.exec_module(dank_browser_backup)

class TestChromeInstalled(unittest.TestCase):
    @patch('dank_browser_backup.subprocess.run')
    def test_chrome_installed_true(self, mock_subprocess_run):
        """Test chrome_installed returns True when subprocess.run succeeds."""
        # Setup the mock to not raise an exception
        mock_subprocess_run.return_value = subprocess.CompletedProcess(
            args=["reg", "query", r"HKLM\SOFTWARE\Clients\StartMenuInternet\Google Chrome", "/v", ""],
            returncode=0,
            stdout="Success"
        )

        result = dank_browser_backup.chrome_installed()

        self.assertTrue(result)
        mock_subprocess_run.assert_called_once_with(
            ["reg", "query", r"HKLM\SOFTWARE\Clients\StartMenuInternet\Google Chrome", "/v", ""],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )

    @patch('dank_browser_backup.subprocess.run')
    def test_chrome_installed_false_called_process_error(self, mock_subprocess_run):
        """Test chrome_installed returns False when subprocess.run raises CalledProcessError."""
        # Setup the mock to raise CalledProcessError (e.g., exit code 1)
        mock_subprocess_run.side_effect = subprocess.CalledProcessError(
            returncode=1,
            cmd=["reg", "query", r"HKLM\SOFTWARE\Clients\StartMenuInternet\Google Chrome", "/v", ""]
        )

        result = dank_browser_backup.chrome_installed()

        self.assertFalse(result)
        mock_subprocess_run.assert_called_once_with(
            ["reg", "query", r"HKLM\SOFTWARE\Clients\StartMenuInternet\Google Chrome", "/v", ""],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )

    @patch('dank_browser_backup.subprocess.run')
    def test_chrome_installed_false_file_not_found(self, mock_subprocess_run):
        """Test chrome_installed returns False when subprocess.run raises FileNotFoundError (e.g., 'reg' command not found)."""
        # Setup the mock to raise FileNotFoundError
        mock_subprocess_run.side_effect = FileNotFoundError()

        result = dank_browser_backup.chrome_installed()

        self.assertFalse(result)
        mock_subprocess_run.assert_called_once_with(
            ["reg", "query", r"HKLM\SOFTWARE\Clients\StartMenuInternet\Google Chrome", "/v", ""],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )

if __name__ == '__main__':
    unittest.main()
