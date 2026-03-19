import sys
import types
import re
import os
import zipfile
import datetime
import importlib.util
import unittest
from unittest.mock import MagicMock, patch, mock_open
def load_module_safely(name, path):
    # We create a dictionary of mocks for the missing or unwanted modules
    mocks = {
        'winreg': MagicMock(),
        'dankware': MagicMock(),
        'psutil': MagicMock(),
        'rich': MagicMock(),
        'rich.align': MagicMock(),
        'rich.console': MagicMock(),
        'rich.live': MagicMock(),
        'rich.panel': MagicMock(),
        'rich.progress': MagicMock(),
        'rich.table': MagicMock(),
        'translatepy': MagicMock()
    }
    with patch.dict('sys.modules', mocks):
        module = types.ModuleType(name)
        with open(path, 'r') as f:
            code = f.read()
        # Remove execution of main() at the end of the script
        code = re.sub(r'^main\(\)$', '', code, flags=re.MULTILINE)
        try:
            exec(code, module.__dict__)
        except Exception as e:
            print(f"Error loading {name}:", e)
        return module
mod = load_module_safely('browser_backup', os.path.join(os.path.dirname(__file__), '..', '__modules__', 'dank.browser-backup.py'))

import unittest

class TestBrowserBackup(unittest.TestCase):
    @patch.object(mod, 'browser_installed')
    @patch('os.path.expandvars')
    @patch('os.path.exists')
    @patch('os.walk')
    @patch('builtins.input')
    @patch.object(mod, 'process_iter')
    @patch('os.get_terminal_size')
    @patch('zipfile.ZipFile')
    @patch('os.remove')
    @patch('os.system')
    @patch('builtins.open', new_callable=mock_open)
    @patch('datetime.datetime')
    @patch.object(mod, 'export_registry_keys')
    @patch('os.getcwd')
    @patch.object(mod, 'translate', side_effect=lambda x: x)
    def test_backup_chrome_happy_path(self, mock_translate, mock_getcwd, mock_export, mock_datetime, mock_file_open, mock_system, mock_remove, mock_zipfile, mock_term_size, mock_process_iter, mock_input, mock_walk, mock_exists, mock_expandvars, mock_browser_installed):
        mock_browser_installed.return_value = True
        mock_expandvars.return_value = "C:\\path\\to\\user\\data"
        mock_exists.return_value = True

        mock_proc = MagicMock()
        mock_proc.info = {"name": "not_chrome.exe"}
        self.mock_process_iter.return_value = [mock_proc]
        self.mock_walk.return_value = [
            ("C:\\path\\to\\user\\data", ["Default"], ["Preferences"]),
            ("C:\\path\\to\\user\\data\\Default", [], ["History", "Bookmarks"])
        ]
        mock_term_size_obj = MagicMock()
        mock_term_size_obj.columns = 80
        self.mock_term_size.return_value = mock_term_size_obj
        mock_now = MagicMock()
        mock_now.strftime.side_effect = ["12-03-2024", "10-30-00-AM"]
        self.mock_datetime.now.return_value = mock_now
        self.mock_getcwd.return_value = "C:\\current\\dir"
        mock_zip_instance = MagicMock()
        self.mock_zipfile.return_value.__enter__.return_value = mock_zip_instance
        self.mock_input.return_value = ""
        mod.backup("Chrome", compression_level=9)

        mock_expandvars.assert_called_with(r"%LOCALAPPDATA%\Google\Chrome\User Data")
        mock_exists.assert_any_call("C:\\path\\to\\user\\data")
        mock_browser_installed.assert_called_once()
        mock_process_iter.assert_called_with(["name"])
        mock_export.assert_called_once_with("HKEY_CURRENT_USER", r"Software\Google\Chrome\PreferenceMACs", export_path="chrome.reg")
        mock_file_open.assert_called_once_with("instructions.txt", "w", encoding="utf-8")

        expected_zip_name = "chrome_12-03-2024_10-30-00-AM.zip"
        self.mock_zipfile.assert_called_once_with(expected_zip_name, "w", zipfile.ZIP_DEFLATED, True, 9, strict_timestamps=False)
        assert mock_zip_instance.write.call_count == 5

        mock_remove.assert_any_call("chrome.reg")
        mock_remove.assert_any_call("instructions.txt")
        mock_system.assert_called_once_with('explorer.exe "C:\\current\\dir"')

    @patch.object(mod, 'browser_installed')
    @patch('os.path.expandvars')
    @patch('os.path.exists')
    @patch('os.walk')
    @patch('builtins.input')
    @patch.object(mod, 'process_iter')
    @patch('os.get_terminal_size')
    @patch('zipfile.ZipFile')
    @patch('os.remove')
    @patch('os.system')
    @patch('builtins.open', new_callable=mock_open)
    @patch('datetime.datetime')
    @patch.object(mod, 'export_registry_keys')
    @patch('os.getcwd')
    @patch.object(mod, 'translate', side_effect=lambda x: x)
    def test_backup_chrome_not_installed(self, mock_translate, mock_getcwd, mock_export, mock_datetime, mock_file_open, mock_system, mock_remove, mock_zipfile, mock_term_size, mock_process_iter, mock_input, mock_walk, mock_exists, mock_expandvars, mock_browser_installed):
        mock_browser_installed.return_value = False
        mock_expandvars.return_value = "C:\\path\\to\\user\\data"
        mock_exists.return_value = True

        mock_proc = MagicMock()
        mock_proc.info = {"name": "not_chrome.exe"}
        self.mock_process_iter.return_value = [mock_proc]
        self.mock_walk.return_value = []
        mock_term_size_obj = MagicMock()
        mock_term_size_obj.columns = 80
        self.mock_term_size.return_value = mock_term_size_obj
        mock_now = MagicMock()
        mock_now.strftime.side_effect = ["12-03-2024", "10-30-00-AM"]
        self.mock_datetime.now.return_value = mock_now
        self.mock_getcwd.return_value = "C:\\current\\dir"
        with patch.object(mod, 'cls') as mock_cls, patch.object(mod, 'clr') as mock_clr:
            mod.backup("Chrome", compression_level=9)
            mock_browser_installed.assert_called_once()
            mock_cls.assert_any_call()
            mock_expandvars.assert_called_with(r"%LOCALAPPDATA%\Google\Chrome\User Data")

    @patch.object(mod, 'browser_installed')
    @patch('os.path.expandvars')
    @patch('os.path.exists')
    @patch('os.walk')
    @patch('builtins.input')
    @patch.object(mod, 'process_iter')
    @patch('os.get_terminal_size')
    @patch('zipfile.ZipFile')
    @patch('os.remove')
    @patch('os.system')
    @patch('builtins.open', new_callable=mock_open)
    @patch('datetime.datetime')
    @patch.object(mod, 'export_registry_keys')
    @patch('os.getcwd')
    @patch.object(mod, 'translate', side_effect=lambda x: x)
    def test_backup_chrome_path_not_exists(self, mock_translate, mock_getcwd, mock_export, mock_datetime, mock_file_open, mock_system, mock_remove, mock_zipfile, mock_term_size, mock_process_iter, mock_input, mock_walk, mock_exists, mock_expandvars, mock_browser_installed):
        mock_browser_installed.return_value = True
        mock_expandvars.return_value = "C:\\path\\to\\user\\data"

        # mock_exists needs to return True eventually for the while loop condition to pass,
        # but also it will be called for the cleanup. Let's just return True for everything
        # after the first False (which simulates path_to_backup not existing initially).
        mock_exists.side_effect = [False, True, True, True, True]
        mock_input.side_effect = ["C:\\valid\\path\\User Data", ""]

        mock_proc = MagicMock()
        mock_proc.info = {"name": "not_chrome.exe"}
        self.mock_process_iter.return_value = [mock_proc]
        self.mock_walk.return_value = []
        mock_term_size_obj = MagicMock()
        mock_term_size_obj.columns = 80
        self.mock_term_size.return_value = mock_term_size_obj
        mock_now = MagicMock()
        mock_now.strftime.side_effect = ["12-03-2024", "10-30-00-AM"]
        self.mock_datetime.now.return_value = mock_now
        self.mock_getcwd.return_value = "C:\\current\\dir"
        with patch.object(mod, 'rm_line') as mock_rm_line, patch.object(mod, 'clr', side_effect=lambda x, *args: x):
            mod.backup("Chrome", compression_level=9)
            self.mock_input.assert_any_call("  > Input user data folder path: ")
            mock_rm_line.assert_called_once()

    @patch.object(mod, 'browser_installed')
    @patch('os.path.expandvars')
    @patch('os.path.exists')
    @patch('os.walk')
    @patch('builtins.input')
    @patch.object(mod, 'process_iter')
    @patch('os.get_terminal_size')
    @patch('zipfile.ZipFile')
    @patch('os.remove')
    @patch('os.system')
    @patch('builtins.open', new_callable=mock_open)
    @patch('datetime.datetime')
    @patch.object(mod, 'export_registry_keys')
    @patch('os.getcwd')
    @patch.object(mod, 'translate', side_effect=lambda x: x)
    def test_backup_chrome_running(self, mock_translate, mock_getcwd, mock_export, mock_datetime, mock_file_open, mock_system, mock_remove, mock_zipfile, mock_term_size, mock_process_iter, mock_input, mock_walk, mock_exists, mock_expandvars, mock_browser_installed):
        mock_browser_installed.return_value = True
        mock_expandvars.return_value = "C:\\path\\to\\user\\data"
        mock_exists.return_value = True

        mock_proc_chrome = MagicMock()
        mock_proc_chrome.info = {"name": "chrome.exe"}
        mock_proc_not_chrome = MagicMock()
        mock_proc_not_chrome.info = {"name": "not_chrome.exe"}
        self.mock_process_iter.side_effect = [[mock_proc_chrome], [mock_proc_not_chrome]]
        self.mock_input.side_effect = ["", ""]
        self.mock_walk.return_value = []
        mock_term_size_obj = MagicMock()
        mock_term_size_obj.columns = 80
        self.mock_term_size.return_value = mock_term_size_obj
        mock_now = MagicMock()
        mock_now.strftime.side_effect = ["12-03-2024", "10-30-00-AM"]
        self.mock_datetime.now.return_value = mock_now
        self.mock_getcwd.return_value = "C:\\current\\dir"
        with patch.object(mod, 'clr', side_effect=lambda x, *args: x):
            mod.backup("Chrome", compression_level=9)
            self.mock_input.assert_any_call("\n  > Chrome is running! Terminate it and press [ENTER]... ")
            assert self.mock_process_iter.call_count == 2
