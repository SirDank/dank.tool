import os
import sys
import requests
import pyminizip
from dankware import cls, clr, sys_open

try: os.chdir(os.path.join(os.environ['USERPROFILE'],'Downloads'))
except: os.chdir("C:\\")

print(clr("\n  > Downloading dank.tool.zip..."))
while True:
    try: data = requests.get("https://github.com/SirDank/dank.tool/raw/main/dank.tool.zip", allow_redirects=True).content; break
    except: input(clr("\n  > Failed to download! Make sure you are connected to the internet! Press [ENTER] to try again... ",2))
try: open("dank.tool.zip","wb").write(data); data = None
except:
    cls(); input(clr("\n  > Failed to save file!\n  > Please manually download the latest version from https://github.com/SirDank/dank.tool/raw/main/dank.tool.zip\n  > Press [ENTER] to EXIT... ",2))
    sys.exit("Failed to save file")

#open("dankware-updater.cmd","w").write(f"@echo off\ntitle dankware-updater\ncolor 0a\ntimeout 3\ndel /F {file_name}\nren dank.tool-latest.exe dank.tool.exe\ncls\necho.\necho =======================\necho.\necho    UPDATE COMPLETE\necho.\necho =======================\necho.\necho    Run dank.tool.exe\necho.\necho =======================\necho.\necho  T E R M I N A T I N G\necho.\ntimeout 3\ndel \"%~f0\" >nul 2>&1\nexit")

print(clr("\n  > Extracting..."))
try: pyminizip.uncompress("dank.tool.zip", "dankware", None, True)
except: 
    cls(); input(clr(f"\n  > Failed to extract!\n  > Please manually extract \"{os.path.join(os.getcwd(), 'dank.tool.zip')}\"\n  > Press [ENTER] to EXIT... ",2))
    sys.exit("Failed to extract")
sys_open("dank.tool-[installer].exe")
os.system("taskkill /f /im dank.tool.exe") # current_version defined in executor.py