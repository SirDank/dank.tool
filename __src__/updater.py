import json
import os
import sys
import webbrowser

import subprocess
import pyminizip
import requests
from colorama import Fore, Style
from dankware import clr, cls, red, rm_line

green_bright = Style.BRIGHT + Fore.GREEN

session = requests.Session()
try:
    DANK_TOOL_VERSION = os.environ["DANK_TOOL_VERSION"]
except:
    exec("DANK_TOOL_VERSION = current_version")  # current_version defined in executor.py < 3.0

# print release notes

try:
    response = session.get("https://api.github.com/repos/SirDank/dank.tool/releases", headers={"User-Agent": f"dank.tool {DANK_TOOL_VERSION}", "Accept": "application/vnd.github.v3+json"}, timeout=3)
    # REMOVE THE BELOW CHECK IN THE FUTURE!
    if response.status_code == 200 and DANK_TOOL_VERSION not in ("2.3.1", "2.3.2", "2.4"):
        releases = response.json()
        if f"v{DANK_TOOL_VERSION}" in (release["tag_name"] for release in releases):
            tmp = []
            for release in releases:
                if f"v{DANK_TOOL_VERSION}" == release["tag_name"]:
                    break
                tmp.append(f"\n{release['tag_name']}\n{release['body']}")

            if tmp:
                print(clr("\n  [ Release Notes ]"))
                for _ in tmp:
                    print(clr(_, colour_two=green_bright))
except:
    pass

# change directory

os.chdir(os.path.dirname(__file__))

branch = "main"
if os.path.isfile("settings.json"):
    with open("settings.json", "r", encoding="utf-8") as file:
        try:
            branch = "dev" if int(json.load(file)["dev-branch"]) else "main"
        except:
            pass

try:
    os.chdir(os.path.join(os.environ["USERPROFILE"], "Downloads"))  # do not use get_path() here
except:
    try:
        os.chdir(os.environ["TEMP"])  # do not use get_path() here
    except:
        os.chdir("C:\\")

# download update

print(clr("\n  - Downloading dank.tool.zip..."))
while True:
    try:
        # stream=True and iter_content() are used here to prevent loading the entire 100MB+ zip file into memory at once
        with session.get(f"https://github.com/SirDank/dank.tool/raw/{branch}/dank.tool.zip", timeout=60, allow_redirects=True, stream=True) as response:
            response.raise_for_status()
            try:
                with open("dank.tool.zip", "wb") as _:
                    for chunk in response.iter_content(chunk_size=8192):
                        _.write(chunk)
                break
            except OSError:
                cls()
                if input(clr(f"\n  - Failed to save file!\n\n  - Would you like to download from [https://github.com/SirDank/dank.tool/raw/{branch}/dank.tool.zip] on a browser?\n\n  > Choice [y/n]: ") + red) == "y":
                    webbrowser.open(f"https://github.com/SirDank/dank.tool/raw/{branch}/dank.tool.zip")
                sys.exit("Failed to save file!")
    except Exception as exc:
        input(clr(f"\n  > Failed to download! {exc} | Press [ENTER] to try again... ", 2))
        rm_line()
        rm_line()

# extract and execute installer

print(clr("\n  - Extracting..."))
try:
    pyminizip.uncompress("dank.tool.zip", "dankware", ".", 0)  # pylint: disable=c-extension-no-member
except:
    subprocess.run(["explorer.exe", "."])
    cls()
    input(clr(f'\n  - Failed to extract!\n\n  - Please manually extract and install from "{os.path.join(os.getcwd(), "dank.tool.zip")}" using the password "dankware"\n\n  > Press [ENTER] to EXIT... ', 2))
    sys.exit("Failed to extract file!")

try:
    os.remove("password = dankware")
except:
    pass
try:
    os.remove("dank.tool.zip")
except:
    pass

try:
    input(clr("\n  > Press [ENTER] to install the latest version of dank.tool... "))
except EOFError:
    pass
subprocess.Popen(["cmd", "/c", "start", "dank.tool-[installer].exe"])
subprocess.run(["taskkill", "/f", "/t", "/im", "dank.tool.exe"])
