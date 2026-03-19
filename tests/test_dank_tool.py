import unittest
from unittest.mock import patch, mock_open, MagicMock
import sys
import importlib.util

class TestDankTool(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # We need to mock some dependencies of dank.tool.py before importing it
        sys.modules['dankware'] = MagicMock()
        sys.modules['rich.align'] = MagicMock()
        sys.modules['rich.columns'] = MagicMock()
        sys.modules['rich.console'] = MagicMock()
        sys.modules['rich.panel'] = MagicMock()
        sys.modules['translatepy'] = MagicMock()
        sys.modules['win11toast'] = MagicMock()
        sys.modules['requests'] = MagicMock()
        sys.modules['dateutil'] = MagicMock()
        sys.modules['dateutil.tz'] = MagicMock()

        # Load module dynamically because of dots in filename
        spec = importlib.util.spec_from_file_location("dank_tool", "__src__/dank.tool.py")
        cls.module = importlib.util.module_from_spec(spec)

        # Mocking sys.exit and builtins to prevent the module from exiting or blocking
        # dank.tool has code running at the module level when imported, such as os.environ checks
        with patch('sys.exit'), patch('builtins.print'), patch('builtins.input'):
            spec.loader.exec_module(cls.module)

    def setUp(self):
        # We also need to set headers for download_assets since it uses module-level 'headers'
        self.module.headers = {"User-Agent": "test-agent"}

    @patch('requests.get')
    def test_download_assets_success(self, mock_get):
        # Arrange
        url = "https://example.com/asset.zip"
        file_name = "test_asset.zip"
        expected_content = b"fake binary data"

        mock_response = MagicMock()
        mock_response.content = expected_content
        mock_get.return_value = mock_response

        mocked_open = mock_open()

        # Act
        with patch('builtins.open', mocked_open):
            self.module.download_assets(url, file_name)

        # Assert
        mock_get.assert_called_once_with(url, headers=self.module.headers, timeout=10)
        mocked_open.assert_called_once_with(file_name, "wb")
        mocked_open().write.assert_called_once_with(expected_content)

    @patch('requests.get')
    def test_download_assets_request_exception(self, mock_get):
        # Arrange
        url = "https://example.com/asset.zip"
        file_name = "test_asset.zip"

        # Simulate an exception during the request
        mock_get.side_effect = Exception("Connection error")
        mocked_open = mock_open()

        # Act & Assert
        with patch('builtins.open', mocked_open):
            with self.assertRaises(Exception) as context:
                self.module.download_assets(url, file_name)

            self.assertEqual(str(context.exception), "Connection error")

        # Assert that get was called
        mock_get.assert_called_once_with(url, headers=self.module.headers, timeout=10)

        # Assert open was NEVER called since get failed
        mocked_open.assert_not_called()

if __name__ == '__main__':
    unittest.main()