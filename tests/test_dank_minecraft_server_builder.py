import unittest
from unittest.mock import patch, MagicMock
import sys
import subprocess
import importlib.util

sys.modules['dankware'] = MagicMock()
sys.modules['translatepy'] = MagicMock()
sys.modules['rich'] = MagicMock()
sys.modules['rich.align'] = MagicMock()
sys.modules['rich.console'] = MagicMock()
sys.modules['requests'] = MagicMock()

class TestDankMinecraftServerBuilder(unittest.TestCase):
    @patch('subprocess.run')
    @patch('os.chdir')
    @patch('os.system')
    @patch('os.makedirs')
    @patch('builtins.print')
    @patch('builtins.open', new_callable=unittest.mock.mock_open)
    @patch('builtins.input')
    @patch('time.sleep')
    def test_java_installation_subprocess(self, mock_sleep, mock_input, mock_open, mock_print, mock_makedirs, mock_system, mock_chdir, mock_run):
        # We need github_file_selector to return a tuple instead of list
        sys.modules['dankware'].github_file_selector.return_value = ("http://example.com/file",)
        sys.modules['dankware'].get_path.return_value = "C:\\"
        sys.modules['dankware'].multithread = MagicMock()
        sys.modules['requests'].get.return_value.json.return_value = {"versions": ["1.20", "1.20.1", "1.20.2", "1.20.4"]}
        sys.modules['requests'].get.return_value.content = b"content"
        sys.modules['requests'].get.return_value.headers = {"Content-Length": "1000"}
        sys.modules['dankware'].clr.side_effect = lambda x, **kwargs: x
        sys.modules['dankware'].red = ""

        # Setup inputs to just pass through
        mock_input.side_effect = [
            'y', '1.20.4', 'TestServer', 'n', 'n', '1024', '1', '', '', '', '', '', '', '', '', ''
        ]

        def mock_run_side_effect(args, **kwargs):
            if args == ["java", "-version"]:
                if not hasattr(mock_run_side_effect, 'failed_once'):
                    mock_run_side_effect.failed_once = True
                    raise subprocess.CalledProcessError(1, args)
                return MagicMock()
            elif args[0] == "winget":
                return MagicMock()
            return MagicMock()

        mock_run.side_effect = mock_run_side_effect

        # Load the module
        spec = importlib.util.spec_from_file_location("builder", "__modules__/dank.minecraft-server-builder.py")
        builder = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(builder)

        # Verify winget call
        winget_called = False
        for call in mock_run.call_args_list:
            if call[0][0][0] == "winget":
                winget_called = True
                self.assertEqual(call[0][0], ["winget", "install", "EclipseAdoptium.Temurin.21.JRE"])
                self.assertTrue(call[1].get('check'))
                break

        self.assertTrue(winget_called, "subprocess.run was not called with winget")
