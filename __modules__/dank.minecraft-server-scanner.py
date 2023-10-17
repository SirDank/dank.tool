import os
import time
import socket
import requests
from translatepy import Translator
from concurrent.futures import ThreadPoolExecutor
from mcstatus import JavaServer, BedrockServer
from dankware import white, white_normal, red, red_normal, red_dim, red
from dankware import multithread, clr, cls, title, align, rm_line, random_ip, get_path

'''

for the future of this script

Goals: masscan port scans

https://github.com/MyKings/python-masscan
https://github.com/Arryboom/MasscanForWindows
https://github.com/rezonmain/mc-server-scanner/blob/main/src/iprange.py
https://github.com/ObscenityIB/creeper/blob/main/creeper.sh
https://raw.githubusercontent.com/robertdavidgraham/masscan/master/data/exclude.conf
https://github.com/Footsiefat/Minecraft-Server-Scanner

'''

def translate(text):
    if DANK_TOOL_LANG:
        try: text = translator.translate(text, source_language='en', destination_language=DANK_TOOL_LANG)
        except: pass
    return text

# checks if ip has a server running on the specified port

def check_java(ip):
    if socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect_ex((ip,port)) == 0:
        save_server(ip)
    
def check_bedrock(ip):
    try:
        socket.socket(socket.AF_INET, socket.SOCK_DGRAM).sendto(b'\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff\x00\xfe\xfe\xfe\xfe\xfd\xfd\xfd\xfd\x124Vx\x00\x00\x00\x00\x00\x00\x00\x00', (ip, port))
        save_server(ip)
    except: pass

def save_server(ip):
    
    try:
    
        if server_type == "java": server = JavaServer(ip,port)
        else: server = BedrockServer(ip,port)
        status = server.status()
        #try: query_response = f"{server.query().software}"
        #except: query_response = ""

        # for https://dashboard.render.com/minecraft-java-servers
        # for https://dashboard.render.com/minecraft-bedrock-servers
        try: executor.submit(requests.post, f"https://dank-site.onrender.com/minecraft-{server_type}-servers", headers={"User-Agent": "dank.tool"}, json={"server_ip":ip})
        except: pass
    
        try:
            response = requests.get(f"http://ipwho.is/{ip}").json()
            if response['success'] == True:
                server_info = f"{response['city']} | {response['connection']['org']} | {response['connection']['domain']}"
            else:
                server_info = "ratelimited on ipwho.is" # 50mil monthly limit
        except: server_info = "ipwho.is is unreachable"

        if server_type == "java":
            to_print = f"{ip} | java | {status.version.name} | {status.players.online}/{status.players.max} online | {int(status.latency)}ms | {server_info} | {status.description}".replace('\n',' ').replace('ü','u')
        elif server_type == "bedrock":
            to_print = f"{ip} | bedrock | {status.version.name} | {status.gamemode} | Map: {status.map_name} | {status.players.online}/{status.players.max} online | {int(status.latency)}ms | {server_info} | {status.motd.raw}".replace('\n',' ')
        
        for _ in ('§0', '§1', '§2', '§3', '§4', '§5', '§6', '§7', '§8', '§9', '§a', '§b', '§c', '§d', '§e', '§f', '§l', '§n', '§o', '§m', '§k', '§r'):
            to_print = to_print.replace(_,'')
        print(clr(f"  > {to_print}\n"))
        open('servers.txt','a',encoding='utf-8').write(f"\n{to_print}")

    except:
        pass

# generates random valid ip

def generate_ip():
    while True:
        ip = random_ip()
        if ip in ips.keys(): continue
        ips[ip] = ""; break

def main():
    
    global ips, server_type, port, translator, DANK_TOOL_LANG
    
    # check if translator is enabled (dank.tool.exe)

    try:
        DANK_TOOL_LANG = os.environ['DANK_TOOL_LANG']
        if DANK_TOOL_LANG == 'en':
            DANK_TOOL_LANG = ''
        else:
            translator = Translator()
    except:
        DANK_TOOL_LANG = ''

    title("𝚍𝚊𝚗𝚔.𝚖𝚒𝚗𝚎𝚌𝚛𝚊𝚏𝚝-𝚜𝚎𝚛𝚟𝚎𝚛-𝚜𝚌𝚊𝚗𝚗𝚎𝚛"); banner = '\n\n     _             _                                                              \n    | |           | |                                                             \n  _ | | ____ ____ | |  _   ____   ____ ___ ___  ____ ____ ____  ____   ____  ____ \n / || |/ _  |  _ \\| | / ) |    \\ / ___|___)___)/ ___) _  |  _ \\|  _ \\ / _  )/ ___)\n( (_| ( ( | | | | | |< ( _| | | ( (___   |___ ( (__( ( | | | | | | | ( (/ /| |    \n \\____|\\_||_|_| |_|_| \\_|_)_|_|_|\\____)  (___/ \\____)_||_|_| |_|_| |_|\\____)_|    \n                                                                                  \n'
    socket.setdefaulttimeout(1)
    
    # get user input
    
    cls(); print(align(clr(banner,4,colours=[white, white_normal, red, red_normal, red_dim])))
    print(clr(f"\n  > Java Server List: https://dank-site.onrender.com/minecraft-java-servers\n\n  > Bedrock Server List: https://dank-site.onrender.com/minecraft-bedrock-servers\n\n  > {translate('You can use the above links to get a list of servers that have been found by the users of this tool')}!"))
    choice = input(clr("\n  > 1: Open Java Server List | 2: Open Bedrock Server List | ENTER: Skip\n\n  > Choice [1/2/ENTER]: ") + red)
    if choice == "1": os.system("start https://dank-site.onrender.com/minecraft-java-servers")
    elif choice == "2": os.system("start https://dank-site.onrender.com/minecraft-bedrock-servers")
    
    # change directory

    try: get_path('Documents')
    except: os.chdir("C:\\")
    try: os.mkdir('dank.mc-server-scanner')
    except FileExistsError: pass
    os.system(f'explorer.exe "dank.mc-server-scanner"')
    os.chdir('dank.mc-server-scanner')
    
    if not os.path.isfile('scan_count.txt'):
        open('scan_count.txt','w').write('0')
    try: open('servers.txt','x').close()
    except: pass
    
    # remove old files

    for _ in ('scanned.txt', 'java_scanned.txt', 'java_scanned.json', 'bedrock_scanned.txt', 'bedrock_scanned.json', 'java_scanned_ips.db', 'bedrock_scanned_ips.db'):
        if os.path.isfile(_): os.remove(_)

    # get user input

    cls(); print(align(clr(banner,4,colours=[white, white_normal, red, red_normal, red_dim])))
    print(clr(f"\n  > {translate('Start with 100 threads and note the performance impact')}.\n\n  > {translate('Generally should be smooth upto 500 threads, you might notice some performance impact above this value')}!\n\n  > {translate('Start with 50000 IPs, it will take a few seconds to generate')}."))

    print("")
    while True:
        server_type = input(clr("  > Server Type [java/bedrock]: ") + red)
        if server_type == "java":
            port = 25565
            break
        elif server_type == "bedrock":
            port = 19132
            break
        else: rm_line()
     
    print("")
    while True:
        threads = input(clr("  > Threads: ") + red)
        if threads.isdigit(): threads = int(threads); break
        else: rm_line()
        
    print("")
    while True:
        ips_amt = input(clr("  > Amount of IPs to scan: ") + red)
        if ips_amt.isdigit(): ips_amt = int(ips_amt); break
        else: rm_line()
        
    # disclaimer
 
    cls(); input(clr(f"\n  [IMPORTANT]\n\n  > {translate('Do not use [ Ctrl + C ] without selecting text first')}!\n\n  > {translate('All the servers are saved to servers.txt')}!\n\n  > {translate('Press [ ENTER ] to start the multithreaded scanner')}... "))
    cls()

    # generate and check ips on multiple threads in batches
    
    gen_rate = 1000 # threads to generate at | higher = faster
    gen_amt = 50000 # max generate / check amount
    gen_rem = ips_amt
    while gen_rem > 0:
        
        ips = {}
        generated = 0
        if not gen_rem >= gen_amt:
            gen_amt = gen_rem
        
        # multithreaded generator
        
        #cls()
        print(clr(f"\n  > Generating {gen_amt} unique ips..."))
        while generated < gen_amt:
            while True:
                try:
                    if gen_amt >= gen_rate:
                        multithread(generate_ip, gen_rate, progress_bar=False); generated += gen_rate
                    else:
                        multithread(generate_ip, gen_amt, progress_bar=False); generated += gen_amt
                    break
                except: input(clr(f"\n  > {translate('Failed to generate ips! Do not use [ Ctrl + C ]! Press [ENTER] to try again')}... ",2)); rm_line()
                
        # multithreaded checker

        while True:
            try: 
                #cls()
                print(clr(f"\n  > Checking {len(ips)} unique ips...\n"))
                if server_type == "java": multithread(check_java, threads, tuple(ips.keys())); break
                else: multithread(check_bedrock, threads, tuple(ips.keys())); break
            except: input(clr(f"\n  > {translate('Failed to check ips! Do not use [ Ctrl + C ]! Press [ENTER] to try again')}... ",2)); rm_line()
        
        # saving scanned ips

        scan_count = int(open('scan_count.txt','r',encoding='utf-8').read())
        scan_count += len(ips)
        open('scan_count.txt','w',encoding='utf-8').write(str(scan_count))
        print(clr(f"\n  > Totally Scanned {scan_count} IPs!"))
        time.sleep(5)
        
        gen_rem -= gen_amt
        
        if gen_rem > 0:
            print(clr(f"\n  > {gen_rem} IPs remaining..."))

if __name__ == "__main__": 

    executor = ThreadPoolExecutor(1000)
    main()
    executor.shutdown(wait=True)
    
    if "DANK_TOOL_VERSION" in os.environ:
        for _ in (ips, server_type, port, executor, check_java, check_bedrock, save_server, generate_ip, main):
            try: del _
            except: pass
