import os
import sys
import requests
import pyminizip
from dankware import cls, clr, green

session = requests.Session()
try: DANK_TOOL_VERSION = os.environ['DANK_TOOL_VERSION']
except: exec("DANK_TOOL_VERSION = current_version") # current_version defined in executor.py < 3.0

# print release notes

try:
    response = session.get("https://api.github.com/repos/SirDank/dank.tool/releases", headers = {"User-Agent": "dank.tool", "Accept": "application/vnd.github.v3+json"})
                                                                # REMOVE THE BELOW CHECK IN THE FAR FUTURE!
    if response.status_code == 200 and not DANK_TOOL_VERSION in ("2.3.1", "2.3.2", "2.4") and f"v{DANK_TOOL_VERSION}" in (release["tag_name"] for release in response.json()):

        tmp = []
        for release in response.json():
            if f"v{DANK_TOOL_VERSION}" == release["tag_name"]:
                break
            tmp.append(f"\n{release['tag_name']}\n{release['body']}")
        
        if tmp:
            print(clr(f"\n  > Release Notes:"))
            for _ in tmp:
                print(clr(_, colour_two=green))
        
except: pass

# change directory

try: os.chdir(os.path.join(os.environ['USERPROFILE'], 'Downloads')) # do not use get_path() here
except: 
    try: os.chdir(os.environ['TEMP']) # do not use get_path() here
    except: os.chdir("C:\\")

# download update

print(clr("\n  > Downloading dank.tool.zip..."))
while True:
    try: data = session.get("https://github.com/SirDank/dank.tool/raw/main/dank.tool.zip", allow_redirects=True).content; break
    except: input(clr("\n  > Failed to download! Make sure you are connected to the internet! Press [ENTER] to try again... ",2))

try: open("dank.tool.zip","wb").write(data); del data
except:
    cls(); input(clr("\n  > Failed to save file!\n  > Please manually download the latest version from https://github.com/SirDank/dank.tool/raw/main/dank.tool.zip\n  > Press [ENTER] to EXIT... ",2))
    sys.exit("Failed to save file!")

# extract and execute installer

print(clr("\n  > Extracting..."))
try: pyminizip.uncompress("dank.tool.zip", "dankware", None, True)
except: 
    cls(); input(clr(f"\n  > Failed to extract!\n  > Please manually extract and install from \"{os.path.join(os.getcwd(), 'dank.tool.zip')}\"\n  > Press [ENTER] to EXIT... ",2))
    sys.exit("Failed to extract file!")
    
try: os.remove("password = dankware")
except: pass
try: os.remove("dank.tool.zip")
except: pass

input(clr("\n  > Press [ENTER] to install the latest version of dank.tool... "))
os.system("start dank.tool-[installer].exe")
os.system("taskkill /f /im dank.tool.exe")
