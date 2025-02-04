import os
import time
import json
import requests
import socketio
import subprocess
import tkinter as tk
from zlib import compress, decompress
from concurrent.futures import ThreadPoolExecutor
from dankware import cls, clr, align, rm_line, green_bright, red, white_normal, blue_bright

if os.name == "nt":
    from win11toast import notify

sio = socketio.Client()

def chatroom_login():

    global username
    url = "https://dank-site.onrender.com/chatroom-login"
    session.post("https://dank-site.onrender.com/chatroom-users", headers=headers) #

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
                        cls(); print(clr(align(f"\n<---|[ Welcome [{username}]! ]|--->\n\n")))
                        break
            break

        match response.status_code:
            case 200: # user already registered
                username = response.content.decode()
                cls(); print(clr(align(f"\n<---|[ Welcome Back [{username}]! ]|--->\n\n")))
                break
            case 401: # unauthorized
                cls(); input(clr("\n  > Unauthorized! Try again in a minute! Press [ENTER] to try again... ",2))

@sio.event
def message(message: bytes):

    allow_notify = False

    message = decompress(message).decode('utf-8')
    if message.startswith("[dank.server]") and (message.endswith(" joined!") or message.endswith(" left!")):
        allow_notify = True
        print(clr(message, colour_two=blue_bright))
    elif message.startswith("[dank.server]"):
        print(clr(message, colour_two=green_bright))
    elif message.startswith("[dank.server-error]"):
        print(clr(message.replace('[dank.server-error]','[dank.server]',1),2))
    elif message.startswith("[SirDank]"):
        if username != 'SirDank':
            allow_notify = True
        print(clr(message.replace("[SirDank]",f"[{green_bright}SirDank{red}]")))
    elif message.startswith(f"[{username}]"):
        print(clr(message))
    else:
        allow_notify = True
        print(clr(message, colour_one=white_normal))

    if notifications and allow_notify:
        executor.submit( # pylint: disable=used-before-assignment
            notify,
            message.split(" - ")[0].replace('[','[ ',1).replace(']',' ]',1),
            message.split(" - ")[1],
            icon = icon,
        )

def chatroom_input():

    global running

    help_msg = clr("[dank.tool] /help - show help\n[dank.tool] /clear - clear chat\n[dank.tool] /notify - enable/disable notifications\n[dank.tool] /users - online users\n[dank.tool] /exit - exit chatroom", colour_two=green_bright)
    print(help_msg)

    def handle_msg(event): # pylint: disable=unused-argument

        global running

        msg = entry.get()
        msg_lower = msg.strip().lower()
        entry.delete(0, tk.END)
        send_msg = False

        if msg == "": return
        if msg_lower.startswith("/"):

            if msg_lower in ("/exit", "/quit", "/bye", "/terminate"):
                running = False

            elif msg_lower in ("/clear", "/cls"):
                cls(); print(clr(align(f"\n<---|[ Welcome Back [{username}]! ]|--->\n\n")))

            elif msg_lower in ("/notify", "/notifications"):
                global notifications
                notifications = not notifications
                print(clr(f"[dank.tool] Notifications {'enabled' if notifications else 'disabled'}!", colour_two=green_bright))

            elif msg_lower == "/help":
                print(help_msg)

            elif msg_lower in ("/users") or username == "SirDank":
                send_msg = True

            else:
                print(clr("[dank.tool] Invalid command! Use /help to view a list of available commands!",2))

        elif len(msg) > 200:
            print(clr("[dank.tool] Message longer than 200 characters!",2))

        elif msg_lower in ("exit", ".exit"):
            print(clr("[dank.tool] Did you mean /exit?",2))

        else:
            send_msg = True

        if send_msg:
            try:
                sio.send(compress(msg.encode('utf-8')))
            except:
                print(clr("[dank.tool] Failed to send!",2))
                running = False

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
    #root.attributes("-topmost", True)
    root.bind('<Button-1>', get_offset)
    root.bind("<B1-Motion>", move_window)
    root.protocol("WM_DELETE_WINDOW", on_closing)
    if icon:
        root.iconbitmap(os.path.join(os.path.dirname(__file__), "dankware.ico"))
    root.configure(highlightthickness=2, bg="#2B2B2B", highlightbackground="#FF0000", borderwidth=1)

    emoji_button = tk.Button(root, text="Emojis", command=toggle_emoji_panel, font=("Consolas", 12), fg="white", bg="#2B2B2B", activebackground="#3A3A3A")
    emoji_button.grid(row=0, column=1, sticky="e", padx=(5, 0))

    entry = tk.Entry(root, bg="#3A3A3A", fg="white", font=("Consolas", 12))
    entry.bind("<Return>", handle_msg)
    entry.grid(row=0, column=0, sticky="ew")

    emoji_frame = tk.Frame(root)
    for i, e in enumerate(["💀", "🗿", "💕", "🔥", "💣", "🤣", "😭", "😡", "😈", "👍"]):
        emoji_button = tk.Button(emoji_frame, text=e, font=("Consolas", 12), fg="white", bg="#2B2B2B", activebackground="#3A3A3A")
        emoji_button.grid(row=i//10, column=i%10)
        emoji_button.bind("<Button-1>", insert_emoji)
    emoji_frame.grid_remove()

    while running:
        root.update()

    root.destroy()
    running = False
    print(clr("[dank.tool] shutting down chatroom...", colour_two=green_bright))

def enable_notifications():

    time.sleep(5)
    if os.name == "nt":
        global notifications
        notifications = True
    del globals()['enable_notifications']

if __name__ == "__main__":

    notifications = False
    session = requests.Session()
    headers={'User-Agent': 'dank.tool', 'Content-Encoding': 'deflate', 'Content-Type': 'application/json'}
    uuid = str(subprocess.check_output(r'wmic csproduct get uuid', stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL, creationflags=0x08000000).decode().split('\n')[1].strip())
    icon = ({'src': f'{os.path.dirname(__file__)}\\dankware.ico', 'placement': 'appLogoOverride'} if os.path.exists(f'{os.path.dirname(__file__)}\\dankware.ico') else None)

    running = True
    chatroom_login()
    executor = ThreadPoolExecutor(5)
    while running:
        try:
            sio.connect('https://dank-site.onrender.com', {'UUID': uuid})
            # rm_line()
            break
        except:
            input(clr("  > Failed to connect! Press [ENTER] to try again... ",2))
            rm_line()
    executor.submit(enable_notifications)
    chatroom_input()
    running = False
    executor.shutdown()

    if "DANK_TOOL_VERSION" in os.environ:
        for _ in ('username', 'session', 'headers', 'uuid', 'icon', 'running', 'notifications', 'x_offset', 'y_offset', 'executor', 'chatroom_login', 'chatroom_connect', 'message', 'chatroom_input', 'sio'):
            if _ in globals(): del globals()[_]
