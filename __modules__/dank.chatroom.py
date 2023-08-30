import os
import time
import json
import requests
import subprocess
import tkinter as tk
from win11toast import notify
from zlib import compress, decompress
from concurrent.futures import ThreadPoolExecutor
from dankware import cls, clr, align, rm_line, green, red, white, white_normal, title

def chatroom_login():
    
    global username
    url = "https://dank-site.onrender.com/chatroom-login"
    
    while True:
        
        cls()
    
        # check if uuid is registered

        while True:
            data = compress(json.dumps({"uuid": uuid}).encode('utf-8'))
            try: response = session.post(url, headers=headers, data=data); break
            except: input(clr("\n  > Failed to login! Make sure you are connected to the internet! Press [ENTER] to try again... ",2))

        # register user
        
        if "missing" in response.content.decode() and response.status_code == 400:
            
            cls(); print(clr(align("\n<---|[ A c c o u n t - C r e a t i o n ]|--->") + "\n\n  > Username must be greater than two characters and less than 16 characters, spaces are not counted!"))
            
            err_msg = ""
            while True:

                username = input(clr(f"\n  > Username{err_msg}: ") + green)
                if len(username.replace(' ','')) < 3:
                    err_msg = f" [{red}too short!]"
                    rm_line(); rm_line(); continue
                elif len(username.replace(' ','')) > 15:
                    err_msg = f" [{red}too long!]"
                    rm_line(); rm_line(); continue
                err_msg = ""

                while True:
                    data = compress(json.dumps({"uuid": uuid, "username": username}).encode('utf-8'))
                    try: response = session.post(url, headers=headers, data=data); break
                    except: input(clr("\n  > Failed to create user! Make sure you are connected to the internet! Press [ENTER] to try again... ",2))

                if response.status_code == 400: # failed to create user
                    err_msg = f" [{red}{response.content.decode()}]"
                    rm_line(); rm_line()
                elif response.status_code == 401: # unauthorized
                    err_msg = f" [{red}Unauthorized! Try again in a minute!]"
                    rm_line(); rm_line()
                elif response.status_code == 200: # successfully created user
                    cls(); print(clr(align(f"\n<---|[ Welcome [{username}]! ]|--->\n")))
                    break
            break

        # user already registered
            
        elif response.status_code == 200:
            username = response.content.decode()
            cls(); print(clr(align(f"\n<---|[ Welcome Back [{username}]! ]|--->\n")))
            break
            
        # unauthorized
        
        elif response.status_code == 401:
            cls(); input(clr("\n  > Unauthorized! Try again in a minute! Press [ENTER] to try again... ",2))

def chat_grabber():
    
    global chat
    global last_msg_id

    session = requests.Session()
    offline_msg = clr("[dank.tool] > You are currently offline!",2)

    while running:
        data = compress(json.dumps({"uuid": uuid, "msg_id": str(printed_msg_id)}).encode('utf-8'))
        try:
            response = json.loads(decompress(session.get("https://dank-site.onrender.com/chatroom", headers=headers, data=data).content).decode('utf-8'))
            chat = str(response["chat"]).splitlines()
            last_msg_id = int(response["msg_id"])
        except:
            if len(chat) > 0 and chat[-1] != offline_msg:
                chat.append(offline_msg)
                print(offline_msg)
        time.sleep(5)
        
def chatroom_output():
    
    global printed_msg_id

    while running:

        if printed_msg_id < last_msg_id and len(chat) > 0:

            for _ in range(len(chat)):
                
                if notifications and not chat[_].startswith(f"[{username}]"):

                    executor.submit(
                        notify,
                        chat[_].split(" > ")[0].replace('[','[ ').replace(']',' ]'),
                        chat[_].split(" > ")[1],
                        icon = {'src': f'{os.path.dirname(__file__)}\\dankware.ico', 'placement': 'appLogoOverride'} if os.path.exists(f'{os.path.dirname(__file__)}\\dankware.ico') else None,
                    )

                if chat[_].startswith("[dank.server]"):
                    chat[_] = clr(chat[_], colour_two=green)
                elif chat[_].startswith("[SirDank]"):
                    chat[_] = clr(chat[_].replace("[SirDank]",f"[{green}SirDank{red}]"))
                elif chat[_].startswith(f"[{username}]"):
                    chat[_] = clr(chat[_])
                else:
                    chat[_] = clr(chat[_], colour_one=white_normal)
            
            print('\n'.join(chat))
            
            printed_msg_id = last_msg_id

        time.sleep(1)

def chatroom_input():
    
    global running
    
    help_msg = clr("[dank.tool] > /help - show help\n[dank.tool] > /clear - clear chatroom\n[dank.tool] > /notify - enable/disable notifications\n[dank.tool] > /exit - exit chatroom", colour_two=green)
    print(help_msg)
    
    def handle_msg(event):

        msg = entry.get()
        msg_lower = msg.lower()
        entry.delete(0, tk.END)
        send_msg = False

        if msg == "": return
        elif msg.startswith("/"):
            
            if msg_lower in ["/exit", "/quit", "/bye", "/terminate"]:
                global running
                running = False
            
            elif msg_lower in ["/clear", "/cls"]:
                cls(); print(clr(align(f"\n<---|[ Welcome Back [{username}]! ]|--->\n")))
            
            elif msg_lower in ["/notify", "/notifications"]:
                global notifications
                notifications = not notifications
                print(clr(f"[dank.tool] > Notifications {'enabled' if notifications else 'disabled'}!", colour_two=green))
            
            elif msg_lower == "/help":
                print(help_msg)
            
            # \n  > /users - show users\n  > /msg <username> <message> - send private message\n  > /pm <username> <message> - send private message\n  > /whisper <username> <message> - send private message\n  > /w <username> <message> - send private message\n  > /private <username> <message> - send private message\n  > /p <username> <message> - send private message\n  > /dm <username> <message> - send private message\n  > /d <username> <message> - send private message\n  > /dm <username> <message> - send private message\n  > /d <username> <message> - send private message\n  > /r <message> - reply to last private message\n  > /reply <message> - reply to last private message\n  > /block <username> - block user\n  > /unblock <username> - unblock user\n  > /b <username> - block user\n  > /u <username> - unblock user\n  > /blocklist - show blocked users\n  > /bl - show blocked users\n  > /blocked - show blocked users\n  > /banned - show banned users\n  > /ban <username> - ban user\n  > /unban <username> - unban user\n  > /b <username> - ban user\n  > /u <username> - unban user\n  > /banlist - show banned users\n  > /bl - show banned users\n  > /banned - show banned users\n  > /kick <username> - kick user\n  > /k <username> - kick user\n  > /kicklist - show kicked users\n  > /kl - show kicked users\n  > /kicked - show kicked users\n  > /kicked - show kicked users\n  > /mute <username> - mute user\n  > /unmute <username> - unmute user\n  > /m <username> - mute user\n  > /u <username> - unmute user\n  > /mutelist - show muted users\n
            
            elif username == "SirDank":
                send_msg = True
                if msg_lower == "/clear-all":
                    global printed_msg_id
                    printed_msg_id = 0
            
            else:
                print(clr("[dank.tool] > Invalid command!",2))
        
        elif len(msg) > 200:
            print(clr("[dank.tool] > Message larger than 200 characters!",2))
        
        else:
            send_msg = True
        
        if send_msg:
            data = compress(json.dumps({"uuid": uuid, "msg": msg}).encode('utf-8'))
            try: session.post("https://dank-site.onrender.com/chatroom", headers=headers, data=data)
            except: print(clr("[dank.tool] > Failed to send!",2))

    def move_window(event):
        root.geometry(f"+{event.x_root}+{event.y_root}")
        
    def on_closing():
        global running
        running = False

    root = tk.Tk()
    root.title("dank.chatroom")
    root.overrideredirect(True)
    root.tk.call("tk::PlaceWindow", root._w, "center")

    root.geometry("300x50")
    root.attributes("-alpha", 0.8)
    root.attributes("-topmost", True)
    root.bind("<B1-Motion>", move_window)
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.iconbitmap(os.path.join(os.path.dirname(__file__), "dankware.ico"))
    root.configure(highlightthickness=2, bg="#2B2B2B", highlightbackground="#FF0000", borderwidth=1) # hot-pink > #FF00FF

    entry = tk.Entry(root, bg="#3A3A3A", fg="white", font=("Consolas", 12))
    entry.bind("<Return>", handle_msg)
    entry.pack(padx=10, pady=10)

    while running:
        root.update()

    root.destroy()
    running = False

if __name__ == "__main__":

    title("𝚍𝚊𝚗𝚔.𝚌𝚑𝚊𝚝𝚛𝚘𝚘𝚖")

    chat = []
    last_msg_id = 0
    printed_msg_id = 0
    notifications = True
    session = requests.Session()
    headers={'User-Agent': 'dank.tool', 'Content-Encoding': 'deflate', 'Content-Type': 'application/json'}
    uuid = str(subprocess.check_output(r'wmic csproduct get uuid', stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL, creationflags=0x08000000).decode().split('\n')[1].strip())

    running = True
    chatroom_login()
    executor = ThreadPoolExecutor(50)
    executor.submit(chat_grabber)
    executor.submit(chatroom_output)
    chatroom_input()
    executor.shutdown(False)
    
    if "DANK_TOOL_VERSION" in os.environ:
        for _ in [chat, last_msg_id, printed_msg_id, session, headers, uuid, running, chatroom_login, executor, chat_grabber, chatroom_output, chatroom_input]:
            try: del _
            except: pass