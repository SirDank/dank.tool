import timeit

setup = """
import json

class MockResponse:
    def __init__(self):
        self.status_code = 200
        # Create a reasonably sized JSON payload simulating Github releases
        self.text = json.dumps([{"tag_name": f"v{i}", "body": "release notes " * 10} for i in range(100, 0, -1)])

    def json(self):
        return json.loads(self.text)

response = MockResponse()
DANK_TOOL_VERSION = "50"
"""

code_original = """
if response.status_code == 200 and DANK_TOOL_VERSION not in ("2.3.1", "2.3.2", "2.4") and f"v{DANK_TOOL_VERSION}" in (release["tag_name"] for release in response.json()):
    tmp = []
    for release in response.json():
        if f"v{DANK_TOOL_VERSION}" == release["tag_name"]:
            break
        tmp.append(f"\\n{release['tag_name']}\\n{release['body']}")
"""

code_optimized = """
if response.status_code == 200 and DANK_TOOL_VERSION not in ("2.3.1", "2.3.2", "2.4"):
    releases = response.json()
    if f"v{DANK_TOOL_VERSION}" in (release["tag_name"] for release in releases):
        tmp = []
        for release in releases:
            if f"v{DANK_TOOL_VERSION}" == release["tag_name"]:
                break
            tmp.append(f"\\n{release['tag_name']}\\n{release['body']}")
"""

n = 10000
t_orig = timeit.timeit(code_original, setup=setup, number=n)
t_opt = timeit.timeit(code_optimized, setup=setup, number=n)

print(f"Original: {t_orig:.4f}s")
print(f"Optimized: {t_opt:.4f}s")
print(f"Improvement: {((t_orig - t_opt) / t_orig) * 100:.2f}% faster")
