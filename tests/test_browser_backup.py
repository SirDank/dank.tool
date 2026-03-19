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

class TestBrowserBackup(unittest.TestCase):
    def setUp(self):
        self.mock_chrome_installed = patch.object(mod, 'chrome_installed').start()
        self.mock_expandvars = patch('os.path.expandvars').start()
        self.mock_exists = patch('os.path.exists').start()
        self.mock_walk = patch('os.walk').start()
        self.mock_input = patch('builtins.input').start()
        self.mock_process_iter = patch.object(mod, 'process_iter').start()
        self.mock_term_size = patch('os.get_terminal_size').start()
        self.mock_zipfile = patch('zipfile.ZipFile').start()
        self.mock_remove = patch('os.remove').start()
        self.mock_system = patch('os.system').start()
        self.mock_file_open = patch('builtins.open', new_callable=mock_open).start()
        self.mock_datetime = patch('datetime.datetime').start()
        self.mock_export = patch.object(mod, 'export_registry_keys').start()
        self.mock_getcwd = patch('os.getcwd').start()
        self.mock_translate = patch.object(mod, 'translate', side_effect=lambda x: x).start()
    def tearDown(self):
        patch.stopall()
    def test_backup_chrome_happy_path(self):
        self.mock_chrome_installed.return_value = True
        self.mock_expandvars.return_value = "C:\\path\\to\\user\\data"
        self.mock_exists.return_value = True
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
        self.mock_expandvars.assert_called_with(r"%LOCALAPPDATA%\Google\Chrome\User Data")
        self.mock_exists.assert_called_once_with("C:\\path\\to\\user\\data")
        self.mock_chrome_installed.assert_called_once()
        self.mock_process_iter.assert_called_with(["name"])
        self.mock_export.assert_called_once_with("HKEY_CURRENT_USER", r"Software\Google\Chrome\PreferenceMACs", export_path="chrome.reg")
        self.mock_file_open.assert_called_once_with("instructions.txt", "w", encoding="utf-8")
        expected_zip_name = "chrome_12-03-2024_10-30-00-AM.zip"
        self.mock_zipfile.assert_called_once_with(expected_zip_name, "w", zipfile.ZIP_DEFLATED, True, 9, strict_timestamps=False)
        assert mock_zip_instance.write.call_count == 5
        self.mock_remove.assert_any_call("chrome.reg")
        self.mock_remove.assert_any_call("instructions.txt")
        self.mock_system.assert_called_once_with('explorer.exe "C:\\current\\dir"')
    def test_backup_chrome_not_installed(self):
        self.mock_chrome_installed.return_value = False
        self.mock_expandvars.return_value = "C:\\path\\to\\user\\data"
        self.mock_exists.return_value = True
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
            self.mock_chrome_installed.assert_called_once()
            mock_cls.assert_any_call()
            self.mock_expandvars.assert_called_with(r"%LOCALAPPDATA%\Google\Chrome\User Data")
    def test_backup_chrome_path_not_exists(self):
        self.mock_chrome_installed.return_value = True
        self.mock_expandvars.return_value = "C:\\path\\to\\user\\data"
        self.mock_exists.side_effect = [False, True]
        self.mock_input.side_effect = ["C:\\valid\\path\\Google\\Chrome\\User Data", ""]
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
    def test_backup_chrome_running(self):
        self.mock_chrome_installed.return_value = True
        self.mock_expandvars.return_value = "C:\\path\\to\\user\\data"
        self.mock_exists.return_value = True
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
