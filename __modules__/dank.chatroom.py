import os
import time
import json
import requests
import subprocess
import tkinter as tk
from win11toast import notify
from zlib import compress, decompress
from concurrent.futures import ThreadPoolExecutor
from dankware import cls, clr, align, rm_line, green_bright, red, white_normal, title

def chatroom_login():

    global username
    url = "https://dank-site.onrender.com/chatroom-login"

    while True:

        cls()

        # check if uuid is registered

        while True:
            data = compress(json.dumps({"uuid": uuid}).encode('utf-8')) # pylint: disable=used-before-assignment
            try: response = session.post(url, headers=headers, data=data); break # pylint: disable=used-before-assignment
            except: input(clr("\n  > Failed to login! Make sure you are connected to the internet! Press [ENTER] to try again... ",2))

        # register user

        if "missing" in response.content.decode() and response.status_code == 400:

            cls(); print(clr(align("\n<---|[ A c c o u n t - C r e a t i o n ]|--->") + "\n\n  - Username must be greater than two characters and lesser than 16 characters, spaces are not counted!"))

            err_msg = ""
            while True:

                username = input(clr(f"\n  > Username{err_msg}: ") + green_bright).strip()
                if len(username.replace(' ','')) < 3:
                    err_msg = f" [{red}too short!]"
                    rm_line(); rm_line(); continue
                if len(username.strip()) > 15:
                    err_msg = f" [{red}too long!]"
                    rm_line(); rm_line(); continue
                err_msg = ""

                while True:
                    data = compress(json.dumps({"uuid": uuid, "username": username}).encode('utf-8'))
                    try: response = session.post(url, headers=headers, data=data); break
                    except: input(clr("\n  > Failed to create user! Make sure you are connected to the internet! Press [ENTER] to try again... ",2))

                match response.status_code:
                    case 400: # failed to create user
                        err_msg = f" [{red}{response.content.decode()}]"
                        rm_line(); rm_line()
                    case 401: # unauthorized
                        err_msg = f" [{red}Unauthorized! Try again in a minute!]"
                        rm_line(); rm_line()
                    case 200: # successfully created user
                        cls(); print(clr(align(f"\n<---|[ Welcome [{username}]! ]|--->\n")))
                        break
            break

        match response.status_code:
            case 200: # user already registered
                username = response.content.decode()
                cls(); print(clr(align(f"\n<---|[ Welcome Back [{username}]! ]|--->\n")))
                break
            case 401: # unauthorized
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
            if len(chat) > 0 and chat[-1] != offline_msg: # pylint: disable=used-before-assignment
                chat.append(offline_msg)
                print(offline_msg)
        time.sleep(5)

def chatroom_output():

    global printed_msg_id

    while running:

        if printed_msg_id < last_msg_id and len(chat) > 0:

            for _, line in enumerate(chat):

                if notifications and not line.startswith(f"[{username}]"):

                    executor.submit( # pylint: disable=used-before-assignment
                        notify,
                        line.split(" > ")[0].replace('[','[ ').replace(']',' ]'),
                        line.split(" > ")[1],
                        icon = {'src': f'{os.path.dirname(__file__)}\\dankware.ico', 'placement': 'appLogoOverride'} if os.path.exists(f'{os.path.dirname(__file__)}\\dankware.ico') else None,
                    )

                if line.startswith("[dank.server]"):
                    chat[_] = clr(line, colour_two=green_bright)
                elif line.startswith("[SirDank]"):
                    chat[_] = clr(line.replace("[SirDank]",f"[{green_bright}SirDank{red}]"))
                elif line.startswith(f"[{username}]"):
                    chat[_] = clr(line)
                else:
                    chat[_] = clr(line, colour_one=white_normal)

            print('\n'.join(chat))

            printed_msg_id = last_msg_id

        time.sleep(1)

def chatroom_input():

    global running

    help_msg = clr("[dank.tool] > /help - show help\n[dank.tool] > /clear - clear chatroom\n[dank.tool] > /notify - enable/disable notifications\n[dank.tool] > /exit - exit chatroom", colour_two=green_bright)
    print(help_msg)

    def handle_msg(event): # pylint: disable=unused-argument

        msg = entry.get()
        msg_lower = msg.lower()
        entry.delete(0, tk.END)
        send_msg = False

        if msg == "": return
        if msg.startswith("/"):

            if msg_lower in ["/exit", "/quit", "/bye", "/terminate"]:
                global running
                running = False

            elif msg_lower in ["/clear", "/cls"]:
                cls(); print(clr(align(f"\n<---|[ Welcome Back [{username}]! ]|--->\n")))

            elif msg_lower in ["/notify", "/notifications"]:
                global notifications
                notifications = not notifications
                print(clr(f"[dank.tool] > Notifications {'enabled' if notifications else 'disabled'}!", colour_two=green_bright))

            elif msg_lower == "/help":
                print(help_msg)

            elif username == "SirDank":
                send_msg = True
                if msg_lower == "/clear-all":
                    global printed_msg_id
                    printed_msg_id = 0

            else:
                print(clr("[dank.tool] > Invalid command!",2))

        elif len(msg) > 200:
            print(clr("[dank.tool] > Message longer than 200 characters!",2))

        elif msg.lower() == "exit":
            print(clr("[dank.tool] > Did you mean /exit?",2))

        else:
            send_msg = True

        if send_msg:
            data = compress(json.dumps({"uuid": uuid, "msg": msg}).encode('utf-8'))
            try: session.post("https://dank-site.onrender.com/chatroom", headers=headers, data=data)
            except: print(clr("[dank.tool] > Failed to send!",2))

    def insert_emoji(event):
        entry.insert(tk.END, event.widget.cget("text"))

    def toggle_emoji_panel():
        if emoji_frame.winfo_viewable():
            emoji_frame.grid_remove()
            root.geometry("300x50")
        else:
            emoji_frame.grid(row=2, column=0, columnspan=2)
            root.geometry("300x100")

    def get_offset(event):
        global x_offset, y_offset
        x_offset = event.x
        y_offset = event.y

    def move_window(event):
        root.geometry(f'+{event.x_root - x_offset}+{event.y_root - y_offset}')

    def on_closing():
        global running
        running = False

    root = tk.Tk()
    root.title("dank.chatroom")
    root.overrideredirect(True)
    root.tk.call("tk::PlaceWindow", root._w, "center") # pylint: disable=protected-access

    root.geometry("300x50")
    root.grid_rowconfigure(1, weight=1)
    root.grid_columnconfigure(0, weight=1)
    root.attributes("-alpha", 0.8)
    root.attributes("-topmost", True)
    root.bind('<Button-1>', get_offset)
    root.bind("<B1-Motion>", move_window)
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.iconbitmap(os.path.join(os.path.dirname(__file__), "dankware.ico"))
    root.configure(highlightthickness=2, bg="#2B2B2B", highlightbackground="#FF0000", borderwidth=1) # hot-pink > #FF00FF

    emoji_button = tk.Button(root, text="Emojis", command=toggle_emoji_panel, font=("Consolas", 12), fg="white", bg="#2B2B2B", activebackground="#3A3A3A")
    emoji_button.grid(row=0, column=1, sticky="e", padx=(5, 0))

    entry = tk.Entry(root, bg="#3A3A3A", fg="white", font=("Consolas", 12))
    entry.bind("<Return>", handle_msg)
    entry.grid(row=0, column=0, sticky="ew")

    emoji_frame = tk.Frame(root)
    for i, e in enumerate(["💀", "🗿", "💕", "🔥", "💣", "🤣", "😭", "😡", "😈", "👍"]):
        emoji_button = tk.Button(emoji_frame, text=e, font=("Consolas", 12), fg="white", bg="#2B2B2B", activebackground="#3A3A3A")
        emoji_button.grid(row=i//5, column=i%5)  # adjust grid size as needed
        emoji_button.bind("<Button-1>", insert_emoji)
    emoji_frame.grid_remove()

    while running:
        root.update()

    root.destroy()
    running = False
    print(clr("[dank.tool] > shutting down chatroom...", colour_two=green_bright))

def enable_notifications():

    time.sleep(10)
    global notifications
    notifications = True
    del globals()['enable_notifications']

if __name__ == "__main__":

    title("𝚍𝚊𝚗𝚔.𝚌𝚑𝚊𝚝𝚛𝚘𝚘𝚖")

    chat = []
    last_msg_id = 0
    printed_msg_id = 0
    notifications = False
    session = requests.Session()
    headers={'User-Agent': 'dank.tool', 'Content-Encoding': 'deflate', 'Content-Type': 'application/json'}
    uuid = str(subprocess.check_output(r'wmic csproduct get uuid', stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL, creationflags=0x08000000).decode().split('\n')[1].strip())

    running = True
    chatroom_login()
    executor = ThreadPoolExecutor(50)
    executor.submit(chat_grabber)
    executor.submit(chatroom_output)
    executor.submit(enable_notifications)
    chatroom_input()
    executor.shutdown()

    if "DANK_TOOL_VERSION" in os.environ:
        for _ in ('username', 'chat', 'last_msg_id', 'printed_msg_id', 'session', 'headers', 'uuid', 'running', 'notifications', 'x_offset', 'y_offset', 'executor', 'chatroom_login', 'chat_grabber', 'chatroom_output', 'chatroom_input'):
            if _ in globals(): del globals()[_]
