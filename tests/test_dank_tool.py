import unittest
from unittest.mock import patch, MagicMock, call
import sys
import os
import builtins
import importlib.util

# Mock dependencies
sys.modules['dankware'] = MagicMock()
sys.modules['translatepy'] = MagicMock()
sys.modules['rich'] = MagicMock()
sys.modules['rich.align'] = MagicMock()
sys.modules['rich.columns'] = MagicMock()
sys.modules['rich.console'] = MagicMock()
sys.modules['rich.panel'] = MagicMock()
sys.modules['requests'] = MagicMock()
sys.modules['dateutil'] = MagicMock()
sys.modules['dateutil.tz'] = MagicMock()

if os.name == 'nt':
    sys.modules['win11toast'] = MagicMock()

# Set up spec
spec = importlib.util.spec_from_file_location("dank_tool", "__src__/dank.tool.py")
dank_tool = importlib.util.module_from_spec(spec)
sys.modules["dank.tool"] = dank_tool

# Since module executes logic at top level, we mock sys.exit, input, and other stuff during import
with patch('sys.exit'), \
     patch('builtins.input', side_effect=EOFError), \
     patch('builtins.print'), \
     patch('builtins.open', MagicMock()), \
     patch('os.system', MagicMock()):

    # Pre-populate variables the script assumes exists in its environment
    dank_tool.DANK_TOOL_VERSION = "1.0.0"
    dank_tool.ONLINE_MODE = False
    dank_tool.COMPATIBILITY_MODE = False
    dank_tool.BRANCH = "main"
    dank_tool.headers = {}

    try:
        spec.loader.exec_module(dank_tool)
    except EOFError:
        pass
    except Exception as e:
        print(f"Module import threw: {e}")

class TestDebugMode(unittest.TestCase):
    """
    Test cases for debug_mode in dank.tool.py.
    """
    @patch('builtins.print')
    @patch('builtins.input', side_effect=['exit'])
    def test_debug_mode_exit(self, mock_input, mock_print):
        """Test that typing 'exit' calls print_modules and breaks the loop."""
        mock_cls = MagicMock()
        mock_print_modules = MagicMock()
        dank_tool.cls = mock_cls
        dank_tool.print_modules = mock_print_modules

        dank_tool.debug_mode()

        mock_cls.assert_called_once()
        mock_input.assert_called_once()
        mock_print_modules.assert_called_once()

    @patch('builtins.print')
    @patch('builtins.input', side_effect=['env', 'exit'])
    def test_debug_mode_env(self, mock_input, mock_print):
        """Test 'env' command."""
        os.environ['TEST_ENV_VAR'] = 'test_value'

        mock_cls = MagicMock()
        mock_print_modules = MagicMock()
        dank_tool.cls = mock_cls
        dank_tool.print_modules = mock_print_modules

        dank_tool.debug_mode()

        self.assertEqual(mock_input.call_count, 2)
        self.assertTrue(mock_print.call_count > 0)

    @patch('builtins.print')
    @patch('builtins.input', side_effect=['globals', 'exit'])
    def test_debug_mode_globals(self, mock_input, mock_print):
        """Test 'globals' command."""
        mock_cls = MagicMock()
        mock_print_modules = MagicMock()
        dank_tool.cls = mock_cls
        dank_tool.print_modules = mock_print_modules

        dank_tool.debug_mode()

        self.assertEqual(mock_input.call_count, 2)
        self.assertTrue(mock_print.call_count > 0)

    @patch('builtins.print')
    @patch('builtins.input', side_effect=['x = 5', 'exit'])
    def test_debug_mode_exec(self, mock_input, mock_print):
        """Test executing a valid Python command."""
        mock_cls = MagicMock()
        mock_print_modules = MagicMock()
        dank_tool.cls = mock_cls
        dank_tool.print_modules = mock_print_modules

        dank_tool.debug_mode()

        self.assertEqual(mock_input.call_count, 2)

    @patch('builtins.print')
    @patch('builtins.input', side_effect=['1 / 0', 'exit'])
    def test_debug_mode_exec_exception(self, mock_input, mock_print):
        """Test executing a command that raises an exception."""
        mock_cls = MagicMock()
        mock_print_modules = MagicMock()
        dank_tool.cls = mock_cls
        dank_tool.print_modules = mock_print_modules

        dank_tool.debug_mode()

        self.assertEqual(mock_input.call_count, 2)
        self.assertTrue(mock_print.call_count > 0)

if __name__ == '__main__':
    unittest.main()
