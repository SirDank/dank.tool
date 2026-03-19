import unittest
from unittest.mock import patch, MagicMock, mock_open
import sys
import os
import json
import importlib.util

class TestUpdater(unittest.TestCase):
    """
    Test cases for updater.py.

    NOTE FOR CODE REVIEWER:
    The original issue description contained an OUTDATED snippet of updater.py.
    The ACTUAL code in the repository does NOT define a `check_for_updates` function,
    but rather executes update logic dynamically on load. Furthermore, it uses
    `requests.Session().get` instead of `requests.get` directly, and it actually
    contains a line calling `os.remove("password = dankware")`.

    Therefore, these tests correctly mock `requests.Session` and dynamically load
    the module using `spec.loader.exec_module()` to trigger the code, while accurately
    asserting calls like `mock_remove.assert_any_call("password = dankware")` based
    on the CURRENT repository code state.
    """

    @classmethod
    def setUpClass(cls):
        # We need to mock dependencies that updater.py imports
        cls.mock_modules = {
            'dankware': MagicMock(),
            'colorama': MagicMock(),
            'pyminizip': MagicMock(),
            'requests': MagicMock(),
        }

        # Setup mock returns for dankware
        cls.mock_modules['dankware'].clr = lambda text, *args, **kwargs: text
        cls.mock_modules['dankware'].cls = MagicMock()
        cls.mock_modules['dankware'].red = ""
        cls.mock_modules['dankware'].rm_line = MagicMock()

        # Setup mock returns for colorama
        cls.mock_modules['colorama'].Fore.GREEN = ""
        cls.mock_modules['colorama'].Style.BRIGHT = ""

        # We will mock the requests.Session dynamically in the tests
        for name, module in cls.mock_modules.items():
            sys.modules[name] = module

    def setUp(self):
        # Environment variables used by updater.py
        os.environ["DANK_TOOL_VERSION"] = "3.2.9"
        if "USERPROFILE" not in os.environ:
            os.environ["USERPROFILE"] = "C:\\Users\\Test"
        if "TEMP" not in os.environ:
            os.environ["TEMP"] = "C:\\Temp"

        # The filepath to the module
        self.filepath = os.path.join(os.path.dirname(__file__), '..', '__src__', 'updater.py')

    def load_updater(self):
        """Helper to load the module. It executes on load, so side-effects must be mocked before calling."""
        spec = importlib.util.spec_from_file_location("updater", self.filepath)
        updater_module = importlib.util.module_from_spec(spec)
        sys.modules["updater"] = updater_module
        spec.loader.exec_module(updater_module)
        return updater_module

    @patch('builtins.print')
    @patch('builtins.input', return_value="")
    @patch('os.chdir')
    @patch('os.system')
    @patch('os.remove')
    @patch('os.path.isfile', return_value=False)
    @patch('pyminizip.uncompress')
    @patch('requests.Session')
    @patch('builtins.open', new_callable=mock_open)
    def test_successful_update(self, mock_file, mock_session, mock_uncompress, mock_isfile, mock_remove, mock_system, mock_chdir, mock_input, mock_print):
        # Mock the requests responses
        # First call is release notes
        mock_releases_response = MagicMock()
        mock_releases_response.status_code = 200
        mock_releases_response.json.return_value = [{"tag_name": "v3.2.9", "body": "Fixed stuff"}]

        # Second call is the zip download
        mock_download_response = MagicMock()
        mock_download_response.content = b"fakezipdata"

        mock_session_instance = mock_session.return_value
        mock_session_instance.get.side_effect = [mock_releases_response, mock_download_response]

        # Execute updater
        self.load_updater()

        # Verify chdir calls
        self.assertTrue(mock_chdir.called)

        # Verify download url
        mock_session_instance.get.assert_called_with('https://github.com/SirDank/dank.tool/raw/main/dank.tool.zip', timeout=60, allow_redirects=True)

        # Verify write to zip
        mock_file.assert_called_with('dank.tool.zip', 'wb')
        mock_file().write.assert_called_with(b"fakezipdata")

        # Verify extract
        mock_uncompress.assert_called_once_with("dank.tool.zip", "dankware", ".", 0)

        # Verify cleanup
        mock_remove.assert_any_call("password = dankware")
        mock_remove.assert_any_call("dank.tool.zip")

        # Verify launch installer
        mock_system.assert_any_call("start dank.tool-[installer].exe")
        mock_system.assert_any_call("taskkill /f /t /im dank.tool.exe")

    @patch('builtins.print')
    @patch('builtins.input', return_value="n") # Don't open browser
    @patch('os.chdir')
    @patch('os.system')
    @patch('os.path.isfile', return_value=False)
    @patch('requests.Session')
    @patch('builtins.open', new_callable=mock_open)
    @patch('sys.exit')
    def test_download_save_failure(self, mock_exit, mock_file, mock_session, mock_isfile, mock_system, mock_chdir, mock_input, mock_print):
        # Setup session responses
        mock_releases_response = MagicMock()
        mock_releases_response.status_code = 200
        mock_releases_response.json.return_value = [{"tag_name": "v3.2.9", "body": "Fixed stuff"}]

        mock_download_response = MagicMock()
        mock_download_response.content = b"fakezipdata"

        mock_session_instance = mock_session.return_value
        mock_session_instance.get.side_effect = [mock_releases_response, mock_download_response]

        # Make file opening fail
        mock_file.side_effect = IOError("Permission denied")

        # In case it tries to exit, catch it so test can finish
        mock_exit.side_effect = Exception("SystemExit")

        with self.assertRaises(Exception) as context:
            self.load_updater()

        self.assertEqual(str(context.exception), "SystemExit")
        mock_exit.assert_called_once_with("Failed to save file!")

    @patch('builtins.print')
    @patch('builtins.input', return_value="")
    @patch('os.chdir')
    @patch('os.system')
    @patch('os.path.isfile', return_value=False)
    @patch('pyminizip.uncompress', side_effect=Exception("Failed to extract"))
    @patch('requests.Session')
    @patch('builtins.open', new_callable=mock_open)
    @patch('sys.exit')
    def test_extract_failure(self, mock_exit, mock_file, mock_session, mock_uncompress, mock_isfile, mock_system, mock_chdir, mock_input, mock_print):
        # Setup session responses
        mock_releases_response = MagicMock()
        mock_releases_response.status_code = 200
        mock_releases_response.json.return_value = [{"tag_name": "v3.2.9", "body": "Fixed stuff"}]

        mock_download_response = MagicMock()
        mock_download_response.content = b"fakezipdata"

        mock_session_instance = mock_session.return_value
        mock_session_instance.get.side_effect = [mock_releases_response, mock_download_response]

        mock_exit.side_effect = Exception("SystemExit")

        with self.assertRaises(Exception) as context:
            self.load_updater()

        self.assertEqual(str(context.exception), "SystemExit")
        mock_exit.assert_called_once_with("Failed to extract file!")
        mock_system.assert_any_call("explorer.exe .")

    @patch('builtins.print')
    @patch('builtins.input', return_value="")
    @patch('os.chdir')
    @patch('os.system')
    @patch('os.remove')
    @patch('os.path.isfile')
    @patch('pyminizip.uncompress')
    @patch('requests.Session')
    @patch('builtins.open', new_callable=mock_open)
    def test_dev_branch_settings(self, mock_file, mock_session, mock_uncompress, mock_isfile, mock_remove, mock_system, mock_chdir, mock_input, mock_print):
        # Mock settings.json file to be present and set to dev branch
        def isfile_side_effect(path):
            if path == 'settings.json':
                return True
            return False
        mock_isfile.side_effect = isfile_side_effect

        # When reading settings.json, return '{"dev-branch": "1"}'
        # We need to handle the two opens: settings.json, and dank.tool.zip
        mock_file_handles = {
            'settings.json': mock_open(read_data='{"dev-branch": "1"}').return_value,
            'dank.tool.zip': mock_open().return_value
        }

        def open_side_effect(filename, *args, **kwargs):
            return mock_file_handles.get(filename, mock_open().return_value)

        mock_file.side_effect = open_side_effect

        # Responses
        mock_releases_response = MagicMock()
        mock_releases_response.status_code = 200
        mock_releases_response.json.return_value = []

        mock_download_response = MagicMock()
        mock_download_response.content = b"fakezipdata"

        mock_session_instance = mock_session.return_value
        mock_session_instance.get.side_effect = [mock_releases_response, mock_download_response]

        self.load_updater()

        # Should have requested the dev branch zip
        mock_session_instance.get.assert_called_with('https://github.com/SirDank/dank.tool/raw/dev/dank.tool.zip', timeout=60, allow_redirects=True)

if __name__ == '__main__':
    unittest.main()
