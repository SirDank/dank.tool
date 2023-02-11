import os
import time
from playsound import playsound
from win10toast import ToastNotifier
from pynput.keyboard import Key, Listener
from pynput.mouse import Button, Controller
from concurrent.futures import ThreadPoolExecutor
from dankware import align, clr, cls, chdir, title, magenta

# sounds

def start():
    try: playsound('start.mp3')
    except: pass
    if notifications: toast.show_toast("dank.auto-clicker","✅ Started",duration = 3,icon_path = f"{os.path.dirname(__file__)}\\dankware.ico",threaded = False)

def stop():
    try: playsound('stop.mp3')
    except: pass
    if notifications: toast.show_toast("dank.auto-clicker","❌ Stopped",duration = 3,icon_path = f"{os.path.dirname(__file__)}\\dankware.ico",threaded = False)

def terminate():
    try: playsound('stop.mp3')
    except: pass

# main

def notify(mode):
    
    if mode == 1: executor.submit(start)
    elif mode == 2: executor.submit(stop)
    elif mode == 3: executor.submit(terminate)

def on_press(key):
    
    global running, paused
    if key == start_key and paused: paused = False; notify(1)
    elif key == stop_key and not pause: pause = True; notify(2)
    elif key == exit_key and running: running = False; notify(3)
    
def main():
    
    global delay, notifications, toast, start_key, stop_key, exit_key, running, paused, executor
    
    banner ="\n\n                                                               \n   _         _             _               _ _     _           \n _| |___ ___| |_   ___ _ _| |_ ___ ___ ___| |_|___| |_ ___ ___ \n| . | .'|   | '_|_| .'| | |  _| . |___|  _| | |  _| '_| -_|  _|\n|___|__,|_|_|_,_|_|__,|___|_| |___|   |___|_|_|___|_,_|___|_|  \n                                                               \n"

    exec(chdir("script"))
    while True:
        try:
            cls(); print(align(clr(banner,4)))
            delay = float(input(clr("\n  > Click Delay in Seconds: ") + magenta))
            break
        except: pass
    notifications = input(clr("\n  > Disable Notifications? [y/n]: ") + magenta).lower()
    if 'y' in notifications: notifications = False
    else: notifications = True
    
    executor = ThreadPoolExecutor()
    toast = ToastNotifier()
    mouse = Controller()
    start_key = Key.f2
    stop_key = Key.f3
    exit_key = Key.f4
    running = True
    paused = True

    print(clr(f"\n  > Controls: Start = {start_key} | Stop = {stop_key} | Exit = {exit_key}".replace("Key.","")))
    toast.show_toast("dank.auto-clicker","😎 Online!",duration = 5,icon_path = f"{os.path.dirname(__file__)}\\dankware.ico",threaded = False)
    
    listener = Listener(on_press=on_press)
    listener.start()
    while running:
        if not paused:
            mouse.click(Button.left, 1)
            time.sleep(delay)
        else:time.sleep(2)
    listener.stop()
    
    executor.shutdown()
    toast.show_toast("dank.auto-clicker","😁 Goodbye!",duration = 5,icon_path = f"{os.path.dirname(__file__)}\\dankware.ico",threaded = False)

if __name__ == "__main__":
    title(f"𝚍𝚊𝚗𝚔.𝚊𝚞𝚝𝚘-𝚌𝚕𝚒𝚌𝚔𝚎𝚛"); main()
