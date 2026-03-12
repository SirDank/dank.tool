import os
import sys
import unittest
import importlib
from unittest.mock import MagicMock, patch
import json
import builtins

class TestExecutor(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # We need to mock all the heavy dependencies that executor.py imports
        cls.mock_modules = {
            'tkinter': MagicMock(),
            'websocket': MagicMock(),
            'dankware': MagicMock(),
            'dankware.tkinter': MagicMock(),
            'pyminizip': MagicMock(),
            'numpy': MagicMock(),
            'perlin_noise': MagicMock(),
            'PIL': MagicMock(),
            'playsound': MagicMock(),
            'psutil': MagicMock(),
            'rich': MagicMock(),
            'rich.align': MagicMock(),
            'rich.console': MagicMock(),
            'socketio': MagicMock(),
            'translatepy': MagicMock(),
            'ursina': MagicMock(),
            'ursina.prefabs': MagicMock(),
            'ursina.prefabs.first_person_controller': MagicMock(),
            'ursina.prefabs.health_bar': MagicMock(),
            'ursina.prefabs.splash_screen': MagicMock(),
            'ursina.scripts': MagicMock(),
            'ursina.scripts.smooth_follow': MagicMock(),
            'direct': MagicMock(),
            'direct.filter': MagicMock(),
            'direct.filter.CommonFilters': MagicMock(),
            'mcstatus': MagicMock(),
            'pypresence': MagicMock(),
            'win11toast': MagicMock(),
            'dateutil': MagicMock(),
            'dateutil.tz': MagicMock()
        }

        # Real packaging import
        cls.mock_modules['packaging'] = importlib.import_module('packaging')
        cls.mock_modules['packaging.version'] = importlib.import_module('packaging.version')

        # Mock requests
        cls.mock_requests = MagicMock()
        cls.mock_response = MagicMock()
        cls.mock_response.content.decode.return_value = "3.2.9"
        cls.mock_requests.Session.return_value.get.return_value = cls.mock_response
        cls.mock_modules['requests'] = cls.mock_requests

        for name, module in cls.mock_modules.items():
            sys.modules[name] = module

        # Ensure tests don't actually run system commands like taskkill
        cls.os_system_patcher = patch('os.system')
        cls.os_system_patcher.start()

        cls.time_sleep_patcher = patch('time.sleep')
        cls.time_sleep_patcher.start()

        cls.sys_exit_patcher = patch('sys.exit')
        cls.sys_exit_patcher.start()

        # Ensure we don't try to submit errors online
        # (magic mock already handles post, but let's make it explicit we don't need patcher)

        # Mock input
        cls.input_patcher = patch('builtins.input', return_value="n")
        cls.input_patcher.start()

        # We need to NOT mock builtins.exec for our `exec(self.code, ...)`
        # Instead, we mock it ONLY during the script execution if it tries to exec updater code.
        # But `exec(self.code)` is how we run it! Let's mock the `code` variable inside globals.


        # Prevent writing to __src__/dank.tool.py by patching builtins.open
        cls.original_open = builtins.open
        def fake_open(file, *args, **kwargs):
            if file == '__src__/dank.tool.py' and 'w' in args:
                return MagicMock()
            return cls.original_open(file, *args, **kwargs)

        cls.open_patcher = patch('builtins.open', side_effect=fake_open)
        cls.open_patcher.start()

        # Save original settings.json if it exists
        cls.original_settings = None
        if os.path.exists('settings.json'):
            with open('settings.json', 'r') as f:
                cls.original_settings = f.read()

        # Load the code, we will execute it into a dict
        with open('__src__/executor.py', 'r') as f:
            cls.code = f.read()

    @classmethod
    def tearDownClass(cls):
        cls.os_system_patcher.stop()
        cls.time_sleep_patcher.stop()
        cls.sys_exit_patcher.stop()

        cls.input_patcher.stop()
        cls.open_patcher.stop()

        if cls.original_settings is not None:
            with open('settings.json', 'w') as f:
                f.write(cls.original_settings)
        elif os.path.exists('settings.json'):
            os.remove('settings.json')

    def setUp(self):
        # We reset the executor dict for every test
        self.exec_globals = {
            '__name__': '__main__',
            '__file__': '__src__/executor.py'
        }
        # Reset response content so it acts normally (version match)
        self.mock_response.content.decode.return_value = "3.2.9"

        if 'DANK_TOOL_LANG' in os.environ:
            del os.environ['DANK_TOOL_LANG']

    def test_settings_json_creation(self):
        # Ensure settings.json logic works
        if os.path.exists('settings.json'):
            os.remove('settings.json')

        # We mock out builtins.exec so that the nested exec(code) in executor.py does not run!
        original_exec = builtins.exec
        def fake_exec(c, *args, **kwargs):
            if c is self.code or isinstance(c, type(compile('','','exec'))):
                original_exec(c, *args, **kwargs)

        with patch('builtins.exec', side_effect=fake_exec):
            compiled_code = compile(self.code, '__src__/executor.py', 'exec')
            original_exec(compiled_code, self.exec_globals)

        self.assertTrue(os.path.exists('settings.json'))
        with open('settings.json', 'r') as f:
            settings = json.load(f)

        self.assertIn('offline-src', settings)
        self.assertIn('offline-mode', settings)
        self.assertIn('dev-branch', settings)

    def test_latest_dank_tool_version_offline(self):
        settings = {
            "offline-src": "1",
            "offline-mode": "1",
            "dev-branch": "0",
            "force-update": "0",
            "force-translate": "0",
            "disable-translate": "0",
            "compatibility-mode": "0",
            "force-startup-audio": "0",
            "disable-startup-audio": "0"
        }
        with open('settings.json', 'w') as f:
            json.dump(settings, f)

        original_exec = builtins.exec
        def fake_exec(c, *args, **kwargs):
            if c is self.code or isinstance(c, type(compile('','','exec'))):
                original_exec(c, *args, **kwargs)

        with patch('builtins.exec', side_effect=fake_exec):
            compiled_code = compile(self.code, '__src__/executor.py', 'exec')
            original_exec(compiled_code, self.exec_globals)

        self.assertEqual(self.exec_globals['LATEST_VERSION'], "0")
        self.assertEqual(self.exec_globals['ONLINE_MODE'], 0)

    def test_latest_dank_tool_version_online(self):
        settings = {
            "offline-src": "0",
            "offline-mode": "0",
            "dev-branch": "0",
            "force-update": "0",
            "force-translate": "0",
            "disable-translate": "0",
            "compatibility-mode": "0",
            "force-startup-audio": "0",
            "disable-startup-audio": "0"
        }
        with open('settings.json', 'w') as f:
            json.dump(settings, f)

        self.mock_response.content.decode.return_value = "9.9.9"

        original_exec = builtins.exec
        def fake_exec(c, *args, **kwargs):
            if c is self.code or isinstance(c, type(compile('','','exec'))):
                original_exec(c, *args, **kwargs)

        with patch('builtins.exec', side_effect=fake_exec):
            compiled_code = compile(self.code, '__src__/executor.py', 'exec')
            original_exec(compiled_code, self.exec_globals)

        self.assertEqual(self.exec_globals['LATEST_VERSION'], "9.9.9")
        self.assertEqual(self.exec_globals['ONLINE_MODE'], 1)

    def test_dank_tool_runs_counter(self):
        original_exec = builtins.exec
        def fake_exec(c, *args, **kwargs):
            if c is self.code or isinstance(c, type(compile('','','exec'))):
                original_exec(c, *args, **kwargs)

        with patch('builtins.exec', side_effect=fake_exec):
            compiled_code = compile(self.code, '__src__/executor.py', 'exec')
            original_exec(compiled_code, self.exec_globals)

        if self.exec_globals.get('ONLINE_MODE') == 1:
             self.assertIn('_executor', self.exec_globals)

    def test_check_system_language_logic(self):
        original_exec = builtins.exec
        def fake_exec(c, *args, **kwargs):
            if c is self.code or isinstance(c, type(compile('','','exec'))):
                original_exec(c, *args, **kwargs)

        with patch('builtins.exec', side_effect=fake_exec):
            compiled_code = compile(self.code, '__src__/executor.py', 'exec')
            original_exec(compiled_code, self.exec_globals)

        self.assertIn("DANK_TOOL_LANG", os.environ)

if __name__ == '__main__':
    unittest.main()
