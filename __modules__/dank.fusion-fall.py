import os
import sys
import json
import time
import shutil
import requests
import pretty_errors
from dankware import align, clr, cls, magenta, white, green, red, reset, err, rm_line, file_selector

def setup():

    try: exec("from wand.image import Image")
    except ImportError:
        cls(); print(clr("\n > MagickWand shared library not found!",2))
        if input(clr("\n > Download ImageMagick? [y/n]: ") + magenta).lower() == "y":
            while True:
                try:

                    file_name = "ImageMagick-7.1.0-37-Q16-HDRI-x64-dll.exe"
                    download_path = os.path.join(os.environ['USERPROFILE'], 'Downloads')
                    if not os.path.exists(download_path):
                        download_path = os.path.join(os.environ['USERPROFILE'], 'Desktop')
                        if not os.path.exists(download_path):
                            download_path = "C:\\"
                    download_path = os.path.join(download_path, file_name)
                    
                    print(clr(f"\n  > Downloading [ {file_name} ]..."))
                    response = requests.get(f"https://github.com/SirDank/dank.tool/raw/main/__assets__/dank.fusion-fall/{file_name}", headers={'user-agent':'dank.tool'}, allow_redirects=True)
                    data = response.content
                    try: size = '{:.3}'.format(int(response.headers['Content-Length'])/1024000)
                    except: size = "?"
                    open(download_path,"wb").write(data)
                    print(clr(f"\n  > Downloaded [ {file_name} ] [ {size} MB ]")); break

                except: input(clr(f"\n  > Failed [ {file_name} ] Press {white}ENTER{red} to try again... ",2))
            
            print(clr("\n  > Launching ImageMagick Installer..."))
            os.system(f'"{download_path}"')
            input(clr("\n  > Press [ENTER] after you have installed ImageMagick... "))
             
        else: raise RuntimeError("MagickWand shared library not found!")

setup()

from wand.image import Image
from unitypackff.asset import Asset
from unitypackff.export import OBJMesh
from unitypackff.object import FFOrderedDict, ObjectPointer
from unitypackff.modding import import_texture, import_mesh, import_audio

# Dependencies for ffextract.py

#import traceback
#from PIL.ImageOps import flip
#from collections import OrderedDict
#from unitypack.export import OBJMesh
#from unitypack.object import ObjectPointer
#from unitypack.environment import UnityEnvironment

def banner():
    
    banner = '\n\n ____  _____ _____ _____   _____ _____    ___ \n|    \\|  _  |   | |  |  | |   __|   __|  |_  |\n|  |  |     | | | |    -|_|   __|   __|  |  _|\n|____/|__|__|_|___|__|__|_|__|  |__|     |___|\n\nx\n\n'
    x = clr(f"by sir.dank | {green}nuclearff.{green}com")
    cls(); print(align(clr(banner,4).replace('x',x)))

def open_workspace():
    
    dankff_path = os.path.join(os.environ['USERPROFILE'], 'Documents')
    if not os.path.exists(dankff_path):
        dankff_path = "C:\\"
    dankff_path = os.path.join(dankff_path, "dank.fusion-fall")
    if not os.path.exists(dankff_path): os.mkdir(dankff_path)
    os.chdir(dankff_path)
    
    banner()

    if len(os.listdir()) == 0:
        
        print(clr("\n  > No workspaces found!",2))
        workspace = input(clr("\n  > New workspace name: ") + magenta)
        os.mkdir(workspace)
        os.chdir(workspace)
    
    else:
        
        print(clr("\n  - Workspaces:\n\n    0 > Create New Workspace"))
        for i, workspace in enumerate(os.listdir()):
            print(clr(f"    {i+1} > {workspace}"))
        
        print()
        while True:
            _ = input(clr("  > Select workspace [num/name]: ") + magenta)
            if _.isdigit() and int(_) >= 0 and int(_) <= len(os.listdir()):
                if int(_) == 0:
                    print()
                    while True:
                        workspace = input(clr("  > New workspace name: ") + magenta)
                        if not os.path.exists(workspace):
                            os.mkdir(workspace); break
                        else: rm_line()
                    break
                else: workspace = os.listdir()[int(_)-1]; break
            elif _ in os.listdir(): workspace = _; break
            else: rm_line()
            
        os.chdir(workspace)
        workspace = os.getcwd()
        if "y" in input(clr("\n  > Open workspace in explorer? [y/n]: ") + magenta).lower():
            os.system(f'explorer.exe "{workspace}"')

def logger(string: str) -> str:

    global log
    log += string + "\n"
    return string

def path_id(filename: str):

    id = ''; data = str(xdtdata).split(filename)[1].split('path_id=')[1]
    for _ in data:
        if _ != ')' and _.isdigit(): id += _
        else: break
    print(clr(f"  > path_id: {id}"))

def dump_xdt():

    output = {}
    for tname, table in xdtdata.items():
        output[tname] = {}
        try:
            for dname, data in table.items(): output[tname][dname] = data
        except: output[tname] = "<err>"
    json.dump(output, open("xdt.json", "w+"), indent=4)

def fix_bundles():

    try: os.mkdir("bundles_to_fix"); input(clr("  > Created bundles_to_fix folder! Hit [ENTER] after adding your files... "))
    except: pass
    try: os.mkdir("fixed_bundles")
    except: pass

    bundles = os.listdir("bundles_to_fix")
    for bundle in bundles:
        original_bytes = open(f"bundles_to_fix/{bundle}", 'rb').read()
        modded_bytes = b'UnityWeb' + original_bytes[original_bytes.find(b'\x00'):]
        open(f"fixed_bundles/{bundle}", 'wb+').write(modded_bytes)

    shutil.rmtree("bundles_to_fix"); print(clr(f"\n  > Fixed [{len(bundles)}] bundles!\n"))

def tswap_mass(dxt_mode):

    try: os.mkdir("tswap_textures"); input(clr("  > Created tswap_textures folder! Hit [ENTER] after adding your files... "))
    except: pass

    textures = os.listdir("tswap_textures")
    for texture in textures:
        try: import_texture(xdtdata, f"tswap_textures/{texture}", texture.split('.')[0], f'dxt{dxt_mode}')
        except: print(clr(err(sys.exc_info()), 2))
        
    print(clr(f"\n  > Mass swapped [{len(textures)}] textures!\n"))

def timport_mass(dxt_mode):
    
    try: os.mkdir("timport_textures"); input(clr("  > Created timport_textures folder! Hit [ENTER] after adding your files... "))
    except: pass

    textures = os.listdir("timport_textures")
    for texture in textures:
        try: 
            new_texture = tabledata.add_object(28)
            import_texture(new_texture._contents, f"timport_textures/{texture}", texture.split('.')[0], f'dxt{dxt_mode}')
            tabledata.add2ab(f"texture/{texture}.dds", new_texture.path_id)
        except: print(clr(err(sys.exc_info()), 2))
        
    print(clr(f"\n  > Mass imported [{len(textures)}] textures!\n"))

def shortcut(mode, cmd, to_exec):

    if mode == 1:
        if "=" not in cmd: exec(f"print({to_exec})".replace('index', cmd))
        else: cmd = cmd.split(' = '); exec(to_exec.replace('index',cmd[0]) + f" = \"{cmd[1]}\"")
    elif mode == 2: 
        if len(cmd) == 1: exec(f"print({to_exec})".replace('index', cmd[0]))
        else: exec(to_exec.replace('index',cmd[0]) + f" = \"{cmd[1]}\"")
    elif mode == 3:
        exec(to_exec)
    print()

def add_npc():
    
    tmp = str(xdtdata['m_pNpcTable']['m_pNpcData'][-1])
    
    if "m_iNpcNumber" not in tmp:
        print(clr('\n  > Could not find "m_iNpcNumber" in str(xdtdata["m_pNpcTable"]["m_pNpcData"][-1])',2))
        return
    
    new_npc_num = int(tmp.split("'m_iNpcNumber', ")[1].split(')')[0]) + 1
    
    data = FFOrderedDict()
    print(clr(f"  > data['m_iNpcNumber'] = {new_npc_num}"))
    data['m_iNpcNumber'] = new_npc_num
    print(clr(f"  > data['m_iNpcName'] = {new_npc_num}"))
    data['m_iNpcName'] = new_npc_num
    print(clr(f"  > data['m_iComment'] = {new_npc_num}"))
    data['m_iComment'] = new_npc_num
    
    new_mesh_num = int(tmp.split("'m_iMesh', ")[1].split(')')[0]) + 1
    print(clr(f"  > data['m_iMesh'] = {new_mesh_num}"))
    data['m_iMesh'] = new_mesh_num
    
    counter = -1
    while True:
        last_barker_num = int(str(xdtdata['m_pNpcTable']['m_pNpcData'][counter]).split("'m_iBarkerNumber', ")[1].split(')')[0])
        if last_barker_num != 0: break
        counter -= 1

    print(clr(f"  > data['m_iBarkerNumber'] = {last_barker_num + 1}"))
    data['m_iBarkerNumber'] = last_barker_num + 1
    
    for index in ['m_iDifficulty', 'm_iTeam', 'm_iNpcLevel', 'm_iNpcType', 'm_iHNpc', 'm_iHNpcNum', 'm_iNpcStyle', 'm_iAiType', 'm_iHP', 'm_iHPRegen', 'm_iDropType', 'm_iRegenTime', 'm_iHeight', 'm_iRadius', 'm_fScale', 'm_iPower', 'm_iAccuracy', 'm_iProtection', 'm_iDodge', 'm_iRunSpeed', 'm_iSwimSpeed', 'm_iJumpHeight', 'm_iJumpDistance', 'm_iSightRange', 'm_iIdleRange', 'm_iCombatRange', 'm_iAtkRange', 'm_iAtkAngle', 'm_iAtkRate', 'm_iEffectArea', 'm_iTargetMode', 'm_iTargetNumber', 'm_iInitalTime', 'm_iDeliverTime', 'm_iDelayTime', 'm_iDurationTime', 'm_iMegaType', 'm_iMegaTypeProb', 'm_iCorruptionType', 'm_iCorruptionTypeProb', 'm_iActiveSkill1', 'm_iActiveSkill1Prob', 'm_iActiveSkill2', 'm_iActiveSkill2Prob', 'm_iActiveSkill3', 'm_iActiveSkill3Prob', 'm_iSupportSkill', 'm_iPassiveBuff', 'm_iNeck', 'm_iTexture', 'm_iTexture2', 'm_iIcon1', 'm_iEffect', 'm_iSound', 'm_iWalkSpeed', 'm_iMapIcon', 'm_iLegStyle', 'm_iBarkerType', 'm_iMegaAni', 'm_iActiveSkill1Ani', 'm_iActiveSkill2Ani', 'm_iSupportSkillAni', 'm_iMegaString', 'm_iCorruptionString', 'm_iActiveSkill1String', 'm_iActiveSkill2String', 'm_iSupportSkillString', 'm_iServiceNumber']:
        while True:
            try: data[index] = int(input(clr(f"  > data['{index}'] (int) = ") + green)); break
            except: pass
            
    for index in ['m_fAnimationSpeed', 'm_fWalkAnimationSpeed', 'm_fRunAnimationSpeed']:
        while True:
            try: data[index] = float(input(clr(f"  > data['{index}'] (float) = ") + green)); break
            except: pass

    print(clr("  > xdtdata['m_pNpcTable']['m_pNpcData'].append(data)"))
    xdtdata['m_pNpcTable']['m_pNpcData'].append(data)

    #data = FFOrderedDict()
    #for index in ['m_iIconNumber', 'm_iIconType']:
    #    while True:
    #        try: data[index] = int(input(clr(f"  > data['{index}'] (int) = ") + green)); break
    #        except: pass
    #print(clr("  > xdtdata['m_pNpcTable']['m_pNpcIconData'].append(data)"))
    #xdtdata['m_pNpcTable']['m_pNpcIconData'].append(data)
    
    data = FFOrderedDict()
    for index in ['m_pstrMMeshModelString', 'm_pstrMTextureString', 'm_pstrMTextureString2', 'm_pstrFTextureString', 'm_pstrFTextureString2', 'm_pstrFMeshModelString']:
        while True:
            try: data[index] = input(clr(f"  > data['{index}'] (string) = ") + green); break
            except: pass
    print(clr("  > xdtdata['m_pNpcTable']['m_pNpcMeshData'].append(data)"))
    xdtdata['m_pNpcTable']['m_pNpcMeshData'].append(data)

    data = FFOrderedDict()
    for index in ['m_strName', 'm_strComment', 'm_strComment1', 'm_strComment2']:
        while True:
            try: data[index] = input(clr(f"  > data['{index}'] (string) = ") + green); break
            except: pass
    while True:
        try: data['m_iExtraNumber'] = int(input(clr(f"  > data['m_iExtraNumber'] (int) = ") + green)); break
        except: pass
    print(clr("  > xdtdata['m_pNpcTable']['m_pNpcBarkerData'].append(data)"))
    xdtdata['m_pNpcTable']['m_pNpcBarkerData'].append(data)
    
    data = FFOrderedDict()
    for index in ['m_strName', 'm_strComment', 'm_strComment1', 'm_strComment2']:
        while True:
            try: data[index] = input(clr(f"  > data['{index}'] (string) = ") + green); break
            except: pass
    while True:
        try: data['m_iExtraNumber'] = int(input(clr(f"  > data['m_iExtraNumber'] (int) = ") + green)); break
        except: pass
    print(clr("  > xdtdata['m_pNpcTable']['m_pNpcStringData'].append(data)"))
    xdtdata['m_pNpcTable']['m_pNpcStringData'].append(data)

# main

def cab():
    
    global tabledata, xdtdata

    print(clr("  > Select Custom Asset Bundle..."))
    cab_path = file_selector("Select Custom Asset Bundle", os.path.join(os.path.dirname(__file__), "dankware.ico"))
    rm_line()
    print(clr(logger(f'  > cab_path = "{cab_path}"')))
    index = int(input(clr('  > TableData Object Index: ') + green))
    cab_name = str(cab_path.split('\\')[-1])
    print(clr(logger(f"  > tabledata = Asset.from_file(open('{cab_path}', 'rb'))")))
    tabledata = Asset.from_file(open(cab_path, 'rb'))
    print(clr(logger(f"  > xdtdata = tabledata.objects[{index}].contents")))
    xdtdata = tabledata.objects[index].contents
    print(clr("\n  > Pre-defined commands: dump-xdt, path_id('filename'), fix-bundles, add-npc, help, log, save, save-all, exit\n"))
    
    help_msg = """  > Available Shortcuts With Examples:\n
 - aimport sound.wav, 22.5, sound  >  new_audio = tabledata.add_object(83); import_audio(new_audio.contents,'sound.wav',22.5,'sound'); tabledata.add2ab('sound.wav',new_audio.path_id)
 - aswap sound.wav, 22.5, sound  >  import_audio(xdtdata,'sound.wav',22.5,'sound')
 - export example.obj  >  open('example.obj','w').write(OBJMesh(xdtdata).export())
 - imesh npc_alienx.obj npc_alienx  >  import_mesh(xdtdata, 'npc_alienx.obj', 'npc_alienx')
 - ms-info  >  print(xdtdata['m_pMissionTable']['m_pMissionData'][1])
 - ms-npc 1 2671  >  xdtdata['m_pMissionTable']['m_pMissionData'][1]['m_iHNPCID'] = NPC_INDEX#
 - ms-npc 1  >  print(xdtdata['m_pMissionTable']['m_pMissionData'][1]['m_iHNPCID'])
 - ms-string 11666 = dee dee's herb garden  >  xdtdata['m_pMissionTable']['m_pMissionStringData'][11666] = \"dee dee's herb garden\"
 - ms-string 11666  >  print(xdtdata['m_pMissionTable']['m_pMissionStringData'][11666])
 - ms-task 1 2  >  xdtdata['m_pMissionTable']['m_pMissionData'][1]['m_iHTaskID'] = 2
 - ms-task 1  >  print(xdtdata['m_pMissionTable']['m_pMissionData'][1]['m_iHTaskID'])
 - ms-tasknext 1 2  >  xdtdata['m_pMissionTable']['m_pMissionData'][1]['m_iSUOutgoingTask'] = 2
 - ms-tasknext 1  >  print(xdtdata['m_pMissionTable']['m_pMissionData'][1]['m_iSUOutgoingTask'])
 - mesh 344  >  print(xdtdata['m_pNpcTable']['m_pNpcMeshData'][344]['m_pstrMMeshModelString'])
 - mesh 344 fusion_cheese  >  xdtdata['m_pNpcTable']['m_pNpcMeshData'][344]['m_pstrMMeshModelString'] = \"fusion_cheese\"
 - meshid 2675 2671  >  xdtdata['m_pNpcTable']['m_pNpcData'][2675]['m_iMesh'] = 2671
 - meshid 2677  >  print(xdtdata['m_pNpcTable']['m_pNpcData'][2675]['m_iMesh'])
 - npc-name 3148 = test name  >  xdtdata['m_pNpcTable']['m_pNpcStringData'][3148]['m_strName'] = \"test name\"
 - npc-name 3148  >  print(xdtdata['m_pNpcTable']['m_pNpcStringData'][3148]['m_strName'])
 - objects 1 1000  >  for _ in range(1,1000): print(f'{_} - {tabledata.objects[_].contents}')
 - texture 344  >  print(xdtdata['m_pNpcTable']['m_pNpcMeshData'][344]['m_pstrMTextureString'])
 - texture 344 fusion_cheese  >  xdtdata['m_pNpcTable']['m_pNpcMeshData'][344]['m_pstrMTextureString'] = \"fusion_cheese\"
 - timport texture 1  >  new_texture = tabledata.add_object(28); import_texture(new_texture._contents,'texture.png','texture','dxt1'); tabledata.add2ab('texture.png',new_texture.path_id)
 - timport texture 5  >  new_texture = tabledata.add_object(28); import_texture(new_texture._contents,'texture.png','texture','dxt5'); tabledata.add2ab('texture.png',new_texture.path_id)
 - timport-mass 1  >  mass import_texture (fmt='dxt1')
 - timport-mass 5  >  mass import_texture (fmt='dxt5')
 - tswap texture.png texture 1  >  import_texture(xdtdata,'texture.png','texture','dxt1')
 - tswap texture.png texture 5  >  import_texture(xdtdata,'texture.png','texture','dxt5')
 - tswap-mass 1  >  mass import_texture (fmt='dxt1')
 - tswap-mass 5  >  mass import_texture (fmt='dxt5')\n"""

    while True:
        try:
            cmd = logger(input(f"  {magenta}> {green}")); print(reset, end=''); cmd_lower = cmd.lower()
            if cmd_lower == "help":
                print(clr(help_msg))
            elif cmd_lower == "exit": break
            elif cmd_lower == "fix-bundles": fix_bundles()
            elif cmd_lower == "add-npc": add_npc()
            elif cmd_lower == "log": open("log.txt","w+").write(log)
            elif cmd_lower == "dump-xdt": 
                try: dump_xdt()
                except: print(clr(err(sys.exc_info()), 2))
            elif cmd_lower == "save":
                try: os.remove(cab_name)
                except: pass
                try: tabledata.save(open(cab_name,'wb'))
                except: print(clr(err(sys.exc_info()), 2))

            elif cmd_lower == "save-all":
                try: dump_xdt()
                except: print(clr(err(sys.exc_info()), 2)); continue
                open("log.txt","w+").write(log)
                try: os.remove(cab_name)
                except: pass
                try: tabledata.save(open(cab_name,'wb'))
                except: print(clr(err(sys.exc_info()), 2)) 

            elif cmd_lower.startswith('aimport '):
                cmd = cmd.replace('aimport ','').split(', ')
                new_audio = tabledata.add_object(83)
                import_audio(new_audio.contents,cmd[0],int(cmd[1]),cmd[2])
                tabledata.add2ab(cmd[0],new_audio.path_id)

            elif cmd_lower.startswith('aswap '):
                cmd = cmd.replace('aswap ','').split(', ')
                import_audio(xdtdata, cmd[0], int(cmd[1]), cmd[2])

            elif cmd_lower.startswith('export '):
                cmd = cmd.replace('export ','').replace(' ','')
                open(cmd,'w').write(OBJMesh(xdtdata).export())

            elif cmd_lower.startswith('imesh '):
                cmd = cmd.replace('imesh ','').split(' ')
                import_mesh(xdtdata, cmd[0], cmd[1])

            elif cmd_lower.startswith('ms-info '):
                print(xdtdata['m_pMissionTable']['m_pMissionData'][int(cmd.replace('ms-info ',''))])

            elif cmd_lower.startswith('ms-npc '):
                cmd = cmd.replace('ms-npc ','').split(' ')
                to_exec = "xdtdata['m_pMissionTable']['m_pMissionData'][index]['m_iHNPCID']"
                shortcut(2, cmd, to_exec)

            elif cmd_lower.startswith('ms-string '):
                cmd = cmd.replace('ms-string ','')
                to_exec = "xdtdata['m_pMissionTable']['m_pMissionStringData'][index]"
                shortcut(1, cmd, to_exec)

            elif cmd_lower.startswith('ms-task '):
                cmd = cmd.replace('ms-task ','').split(' ')
                to_exec = "xdtdata['m_pMissionTable']['m_pMissionData'][index]['m_iHTaskID']"
                shortcut(2, cmd, to_exec)

            elif cmd_lower.startswith('ms-tasknext '):
                cmd = cmd.replace('ms-tasknext ','').split(' ')
                to_exec = "xdtdata['m_pMissionTable']['m_pMissionData'][index]['m_iSUOutgoingTask']"
                shortcut(2, cmd, to_exec)

            elif cmd_lower.startswith('mesh '):
                cmd = cmd.replace('mesh ','').split(' ')
                to_exec = "xdtdata['m_pNpcTable']['m_pNpcMeshData'][index]['m_pstrMMeshModelString']"
                shortcut(2, cmd, to_exec)

            elif cmd_lower.startswith('meshid '):
                cmd = cmd.replace('meshid ','').split(' ')
                to_exec = "xdtdata['m_pNpcTable']['m_pNpcData'][index]['m_iMesh']"
                shortcut(2, cmd, to_exec)

            elif cmd_lower.startswith('npc-name '):
                cmd = cmd.replace('npc-name ','')
                to_exec = "xdtdata['m_pNpcTable']['m_pNpcStringData'][index]['m_strName']"
                shortcut(1, cmd, to_exec)

            elif cmd_lower.startswith('objects '):
                cmd = cmd.replace('objects ','').split(' ')
                to_exec = f"for _ in range({cmd[0]},{cmd[1]}): print(f'{{_}} - {{tabledata.objects[_].contents}}')"
                shortcut(3, cmd, to_exec)

            elif cmd_lower.startswith('texture '):
                cmd = cmd.replace('texture ','').split(' ')
                to_exec = "xdtdata['m_pNpcTable']['m_pNpcMeshData'][index]['m_pstrMTextureString']"
                shortcut(2, cmd, to_exec)

            elif cmd_lower.startswith('timport '):
                cmd = cmd.replace('timport ','').split(' ')
                new_texture = tabledata.add_object(28)
                import_texture(new_texture._contents, f'{cmd[0]}.png', cmd[0], f'dxt{cmd[1]}')
                tabledata.add2ab(f"texture/{cmd[0]}.dds", new_texture.path_id)

            elif cmd_lower.startswith('timport-mass '):
                cmd = cmd.replace('timport-mass ','').replace(' ','')
                timport_mass(cmd)

            elif cmd_lower.startswith('tswap '):
                cmd = cmd.replace('tswap ','').split(' ')
                import_texture(xdtdata, cmd[0], cmd[1], f'dxt{cmd[2]}')

            elif cmd_lower.startswith('tswap-mass '):
                cmd = cmd.replace('tswap-mass ','').replace(' ','')
                tswap_mass(cmd)

            else:
                exec(cmd); print()

        except: print(clr(err(sys.exc_info()) + '\n', 2))

def main():
    
    sys.setrecursionlimit(10000)
    open_workspace()
    
    while True:
        
        banner(); print(clr(f"\n  1 > CAB Explorer / Editor\n  2 > Fix Bundles\n  3 > Mission Builder (coming soon)\n  4 > Change workspace [{os.path.basename(os.getcwd())}]\n  5 > Visit {green}nuclearff.{green}com{white}\n  6 > Exit\n"))
        
        choice = input(clr("  > Choice: ") + green)
        if choice == "1": banner(); cab()
        elif choice == "2": banner(); fix_bundles()
        #elif choice == "3": banner(); mission_builder()
        elif choice == "4": open_workspace()
        elif choice == "5": os.system(f'start https://nuclearff.com/')
        elif choice == "6": break
        else: rm_line()

if __name__ == '__main__':
    log = ''
    main()

