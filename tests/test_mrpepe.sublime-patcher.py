import importlib.util
import sys
import unittest

spec = importlib.util.spec_from_file_location('mrpepe_sublime_patcher', '__modules__/mrpepe.sublime-patcher.py')
sublime_patcher = importlib.util.module_from_spec(spec)
sys.modules['mrpepe_sublime_patcher'] = sublime_patcher
spec.loader.exec_module(sublime_patcher)

class TestIsPatched(unittest.TestCase):
    def test_is_patched_with_unpatched_data(self):
        # Data containing the target unpatched byte sequence
        unpatched_sequence = b"\x80\x78\x05\x00\x0F\x94\xC1"
        data = b"some prefix bytes" + unpatched_sequence + b"some suffix bytes"
        self.assertFalse(sublime_patcher.is_patched(data))

    def test_is_patched_with_patched_data(self):
        # Data without the target byte sequence (simulating patched or unrelated data)
        # Using the same length but different bytes to simulate a patch
        patched_sequence = b"\x90\x90\x90\x90\x90\x90\x90" # e.g. NOPs
        data = b"some prefix bytes" + patched_sequence + b"some suffix bytes"
        self.assertTrue(sublime_patcher.is_patched(data))

    def test_is_patched_with_empty_data(self):
        # Empty data shouldn't contain the sequence, so it's considered "patched" or at least not unpatched
        self.assertTrue(sublime_patcher.is_patched(b""))

    def test_is_patched_with_partial_match(self):
        # Data containing a partial match of the sequence
        partial_sequence = b"\x80\x78\x05\x00\x0F\x94" # Missing the last byte
        data = b"some prefix bytes" + partial_sequence + b"some suffix bytes"
        self.assertTrue(sublime_patcher.is_patched(data))

if __name__ == '__main__':
    unittest.main()
