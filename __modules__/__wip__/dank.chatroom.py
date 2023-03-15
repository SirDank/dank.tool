
import sys
import time
import requests
from concurrent.futures import ThreadPoolExecutor

# chatroom user validator

def dank_tool_chatroom():
    global chatroom_users
    session = requests.Session()
    url = "https://dank-site.onrender.com/chatroom-users"
    while True:
        try: session.post(url) # validator
        except: pass
        #print(tmp.content.decode(), tmp.status_code) ###
        try: chatroom_users = session.get(url, headers={"User-Agent": "dank.tool"}).content.decode()
        except: chatroom_users = "?"
        #print(chatroom_users) ###
        time.sleep(240)
ThreadPoolExecutor(10).submit(dank_tool_chatroom)

### start








import os
import time
import json
import requests
import subprocess
from pynput.keyboard import Listener
from dankware import cls, clr, align, rm_line, white, green, red, err

session = requests.Session()
uuid = str(subprocess.check_output(r'wmic csproduct get uuid',creationflags=0x08000000).decode().split('\n')[1].strip())

def chatroom_login():
    
    global username
    url = "https://dank-site.onrender.com/chatroom-login"
    
    while True:
        
        cls()
    
        # check if uuid registered

        while True:
            try: response = session.post(url, headers={"uuid": uuid}, timeout=3); break
            except: input(clr("\n  > Failed to login! Make sure you are connected to the internet! Press [ENTER] to try again... ",2))

        # register user
        
        if "not found" in response.content.decode() and response.status_code == 400:
            
            cls(); print(clr(align("\n<---|[ A c c o u n t - C r e a t i o n ]|--->") + "\n\n  > Username must be greater than two characters and less than 16 characters, spaces are not counted!"))
            
            err_msg = ""
            while True:

                username = input(clr(f"\n  > Username{err_msg}: ") + green)
                if len(username.replace(' ','')) < 3:
                    err_msg = f" [{red}too short!]"; rm_line(); rm_line(); continue
                elif len(username.replace(' ','')) > 15:
                    err_msg = f" [{red}too long!]"; rm_line(); rm_line(); continue

                while True:
                    try: response = session.post(url, headers={"uuid": uuid, "username": username}, timeout=3); break
                    except: input(clr("\n  > Failed to create user! Make sure you are connected to the internet! Press [ENTER] to try again... ",2))

                if response.status_code == 400: # failed to create user
                    err_msg = f" [{red}{response.content.decode()}]"
                    rm_line(); rm_line()
                elif response.status_code == 200: # successfully created user
                    break
            break

        # user already registered
            
        elif response.status_code == 200:
            username = response.content.decode()
            cls(); print(clr(align(f"\n<---|[ Welcome Back [{username}]! ]|--->\n")))
            break
            
        # unauthorized
        
        elif response.status_code == 401:
            cls(); input("\n  > Unauthorized! Try again in a minute! Press [ENTER] to try again... ",2)

def on_press(key):
    keys_pressed.append(key)

def on_release(key):
    time.sleep(5)
    try: keys_pressed.remove(key)
    except: pass

def keypress_watcher():
    
    global keys_pressed
    keys_pressed = []
    
    listener = Listener(on_press = on_press, on_release = on_release)
    listener.start()
    while running: time.sleep(60)
    listener.stop()

def chat_grabber():
    
    global chat
    global last_msg_id

    chat = []
    last_msg_id = 0
    session = requests.Session()
    offline_msg = clr("[dank.tool] > You are currently offline!",2)

    while running:
        
        if not taking_input:

            try: 
                response = json.loads(session.get("https://dank-site.onrender.com/chatroom", headers={"uuid": uuid, "msg_id": str(printed_msg_id)}, timeout=3).content.decode())
                chat = str(response["chat"]).splitlines()
                last_msg_id = int(response["msg_id"])
                try: chat.remove(offline_msg)
                except: pass
            except:
                #print(clr(sys.exc_info(),2))
                if len(chat) > 0 and chat[-1] != offline_msg:
                    chat.append(offline_msg)
        time.sleep(3)
        
def chatroom_output():
    
    global printed_msg_id

    printed_msg_id = 0
    
    while running:

        if not taking_input:

            while len(keys_pressed) > 0:
                time.sleep(5)
            if printed_msg_id < last_msg_id:
                print(clr('\n'.join(chat)))
                printed_msg_id = last_msg_id
        time.sleep(2.5)

def chatroom_input():
    
    global keys_pressed
    global taking_input
    
    while running:
        
        if len(keys_pressed) > 0:
            
            taking_input = True
            msg = input(clr(f"[{username}] > " + white, colour_two=green))

            rm_line()
            if msg == "exit": break
            elif len(msg) > 200: print(clr("[dank.tool] > Failed to send because message larger than 200 characters!",2))
            #elif len(msg.replace(' ','')): print(clr("[dank.tool] > Failed to send empty message!",2))

            try: session.post("https://dank-site.onrender.com/chatroom", headers={"uuid": uuid, "msg": msg}, timeout=3)
            except: print(clr("[dank.tool] > Failed to send!",2))
            keys_pressed = []
            taking_input = False
            
        else:
            
            taking_input = False
        
        time.sleep(0.5)

running = True
chatroom_login()
executor = ThreadPoolExecutor()
executor.submit(keypress_watcher)
executor.submit(chat_grabber)
executor.submit(chatroom_output)
chatroom_input()
running = False

### end

#print(username, uuid)