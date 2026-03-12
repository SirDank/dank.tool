import os
import sys

# Add parent directory to path so we can import modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '__modules__')))

# Load the module
import importlib.util
patcher_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '__modules__', 'mrpepe.sublime-patcher.py'))
spec = importlib.util.spec_from_file_location("mrpepe_patcher", patcher_path)
patcher = importlib.util.module_from_spec(spec)

# Mock some dependencies to avoid runtime errors when loading the module
import types
sys.modules['dankware'] = types.ModuleType('dankware')
sys.modules['dankware'].align = lambda x: x
sys.modules['dankware'].clr = lambda x, colour_two=None: x
sys.modules['dankware'].cls = lambda: None
sys.modules['dankware'].cyan = 'cyan'
sys.modules['dankware'].fade = lambda x, y: x
sys.modules['dankware'].green_bright = 'green'
sys.modules['dankware'].magenta = 'magenta'
sys.modules['dankware'].white_bright = 'white'
sys.modules['dankware'].yellow_bright = 'yellow'

spec.loader.exec_module(patcher)

def test_is_patched():
    print("Testing is_patched()...")

    # Test 1: None data
    print("  Test 1: None data")
    assert patcher.is_patched(None) == False

    # Test 2: Empty bytes
    print("  Test 2: Empty bytes")
    assert patcher.is_patched(b"") == False

    # Test 3: Short data
    print("  Test 3: Short data")
    assert patcher.is_patched(b"\x00\x01\x02") == False

    # Create mock patched data that matches what the function looks for
    # The max offset is 0x001C6CFB (1862907), so we need an array at least that big
    max_offset = 0x001C6CFB
    patched_data = bytearray(max_offset + 1)
    for offset, value in patcher.offsets_and_values.items():
        patched_data[offset] = value

    # Test 4: Fully patched data
    print("  Test 4: Fully patched data")
    assert patcher.is_patched(patched_data) == True

    # Test 5: Unpatched data (modify one byte)
    print("  Test 5: Unpatched data")
    unpatched_data = bytearray(patched_data)
    unpatched_data[0x00030170] = 0xFF # Different from the expected 0x00
    assert patcher.is_patched(unpatched_data) == False

    print("All tests passed!")

if __name__ == "__main__":
    test_is_patched()