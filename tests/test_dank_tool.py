import sys
import os
import builtins
import unittest
from unittest.mock import MagicMock, patch
import importlib.util

class TestDankToolMenuRequestResponsesApi(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Setup environment to avoid execution side-effects
        cls.os_environ_patcher = patch.dict('os.environ', {'DANK_TOOL_VERSION': '1.0', 'DANK_TOOL_ONLINE': '1'})
        cls.os_environ_patcher.start()

        # Mock inputs to prevent hanging
        cls.input_patcher = patch('builtins.input', return_value="exit")
        cls.input_patcher.start()

        cls.exit_patcher = patch('sys.exit')
        cls.exit_patcher.start()

        cls.system_patcher = patch('os.system')
        cls.system_patcher.start()

        cls.sleep_patcher = patch('time.sleep')
        cls.sleep_patcher.start()

        cls.mock_modules = {
            'requests': MagicMock(),
            'dankware': MagicMock(),
            'rich': MagicMock(),
            'rich.align': MagicMock(),
            'rich.columns': MagicMock(),
            'rich.console': MagicMock(),
            'rich.panel': MagicMock(),
            'translatepy': MagicMock(),
            'dateutil': MagicMock(),
            'dateutil.tz': MagicMock(),
            'win11toast': MagicMock()
        }

        # Important functions inside dankware
        cls.mock_modules['dankware'].clr = lambda text, *args, **kwargs: text
        cls.mock_modules['dankware'].get_duration = lambda *args, **kwargs: "5 mins"

        for name, module in cls.mock_modules.items():
            sys.modules[name] = module

        # Import the module dynamically
        filepath = os.path.join(os.path.dirname(__file__), '..', '__src__', 'dank.tool.py')
        spec = importlib.util.spec_from_file_location("dank_tool", filepath)
        cls.dank_tool = importlib.util.module_from_spec(spec)
        sys.modules['dank_tool'] = cls.dank_tool

        # IMPORTANT: Avoid exec_module modifying local execution.
        # But we MUST successfully load it. So we don't mock exec!
        # We only mock builtins.open to avoid write issues.
        with patch('builtins.open', new_callable=MagicMock):
            spec.loader.exec_module(cls.dank_tool)

    @classmethod
    def tearDownClass(cls):
        cls.os_environ_patcher.stop()
        cls.input_patcher.stop()
        cls.exit_patcher.stop()
        cls.system_patcher.stop()
        cls.sleep_patcher.stop()

        for name in cls.mock_modules:
            sys.modules.pop(name, None)
        sys.modules.pop('dank_tool', None)

    def setUp(self):
        self.dank_tool.menu_request_responses = {}
        self.dank_tool.headers = {'User-Agent': 'dank.tool/1.0'}
        self.dank_tool.DEV_BRANCH = False
        import requests
        self.requests_mock = requests

        # We also need to patch the original requests reference directly inside dank_tool
        # just in case it's doing something weird.
        self.dank_tool.requests = self.requests_mock

        # Reset side effect
        self.requests_mock.get.side_effect = None

    def test_get_menu_request_responses_api_success(self):
        # Setup mock response to match updated_on expectations
        mock_response = MagicMock()
        mock_response.json.return_value = [{"commit": {"author": {"date": "2023-10-01T12:00:00Z"}}}]
        self.requests_mock.get.return_value = mock_response

        # Need to patch datetime to avoid exceptions in updated_on
        mock_datetime = MagicMock()
        mock_datetime.datetime.now.return_value = MagicMock()
        mock_datetime.datetime.return_value = MagicMock()

        # Call function directly via dank_tool
        with patch.object(self.dank_tool, 'datetime', mock_datetime):
            self.dank_tool.get_menu_request_responses_api("SirDank/test_repo")

        # Verify output
        self.assertIn("SirDank/test_repo", self.dank_tool.menu_request_responses)
        self.assertEqual(self.dank_tool.menu_request_responses["SirDank/test_repo"], "[bright_green]🔄 5 mins ago")
        self.requests_mock.get.assert_called_with(
            "https://api.github.com/repos/SirDank/test_repo/commits?path=.&page=1&per_page=1",
            headers=self.dank_tool.headers,
            timeout=3
        )

    def test_get_menu_request_responses_api_network_error(self):
        # Setup mock to raise a connection error
        self.requests_mock.get.side_effect = Exception("Connection Refused")

        # Call function
        self.dank_tool.get_menu_request_responses_api("SirDank/test_repo")

        # Verify output fallback
        self.assertIn("SirDank/test_repo", self.dank_tool.menu_request_responses)
        self.assertEqual(self.dank_tool.menu_request_responses["SirDank/test_repo"], "")

    def test_get_menu_request_responses_api_timeout(self):
        # Setup mock to raise a timeout error
        self.requests_mock.get.side_effect = Exception("Read Timeout")

        # Call function
        self.dank_tool.get_menu_request_responses_api("SirDank/test_repo")

        # Verify output fallback
        self.assertIn("SirDank/test_repo", self.dank_tool.menu_request_responses)
        self.assertEqual(self.dank_tool.menu_request_responses["SirDank/test_repo"], "")

    def test_get_menu_request_responses_api_http_error(self):
        # Setup mock to raise an HTTP error
        self.requests_mock.get.side_effect = Exception("404 Not Found")

        # Call function
        self.dank_tool.get_menu_request_responses_api("SirDank/test_repo")

        # Verify output fallback
        self.assertIn("SirDank/test_repo", self.dank_tool.menu_request_responses)
        self.assertEqual(self.dank_tool.menu_request_responses["SirDank/test_repo"], "")

    def test_get_menu_request_responses_api_invalid_json(self):
        # Setup mock to return invalid format JSON
        mock_response = MagicMock()
        mock_response.json.return_value = {}  # Empty dict instead of list of dicts
        self.requests_mock.get.return_value = mock_response

        # Call function
        self.dank_tool.get_menu_request_responses_api("SirDank/test_repo")

        # Verify output fallback
        self.assertIn("SirDank/test_repo", self.dank_tool.menu_request_responses)
        self.assertEqual(self.dank_tool.menu_request_responses["SirDank/test_repo"], "[red1][[red] unreleased [red1]]")

    def test_get_menu_request_responses_api_internal_repo(self):
        # Setup mock response to match updated_on expectations for internal repo
        mock_response = MagicMock()
        mock_response.json.return_value = [{"commit": {"author": {"date": "2023-10-01T12:00:00Z"}}}]
        self.requests_mock.get.return_value = mock_response

        # Need to patch datetime to avoid exceptions in updated_on
        mock_datetime = MagicMock()
        mock_datetime.datetime.now.return_value = MagicMock()
        mock_datetime.datetime.return_value = MagicMock()

        # Call function directly via dank_tool
        with patch.object(self.dank_tool, 'datetime', mock_datetime):
            self.dank_tool.get_menu_request_responses_api("dank.game")

        # Verify output
        self.assertIn("dank.game", self.dank_tool.menu_request_responses)
        self.assertEqual(self.dank_tool.menu_request_responses["dank.game"], "[bright_green]🔄 5 mins ago")
        self.requests_mock.get.assert_called_with(
            "https://api.github.com/repos/SirDank/dank.tool/commits?path=__modules__/dank.game.py&page=1&per_page=1",
            headers=self.dank_tool.headers,
            timeout=3
        )


if __name__ == '__main__':
    unittest.main()
