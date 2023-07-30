import os
import sys
import json
import time
import shutil
import requests
import pretty_errors
from dankware import align, clr, cls, err, rm_line, file_selector, title
from dankware import white, white_normal, red, red_normal, red_dim, green, reset

title("𝚍𝚊𝚗𝚔.𝚏𝚞𝚜𝚒𝚘𝚗-𝚏𝚊𝚕𝚕")

def setup():
    
    global magickwand_installed

    try: exec("from wand.image import Image"); magickwand_installed = True
    except ImportError:
        
        magickwand_installed = False

        cls(); print(clr("\n  > MagickWand shared library not found!",2))
        
        if input(clr("\n  > Download ImageMagick? [y/n]: ") + red).lower() == "y":
    
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
            magickwand_installed = True

setup()

if magickwand_installed:

    from wand.image import Image
    from unitypackff.asset import Asset
    from unitypackff.export import OBJMesh
    from unitypackff.object import FFOrderedDict, ObjectPointer
    from unitypackff.modding import import_texture, import_mesh, import_audio

def banner():
    
    banner = '\n\n ____  _____ _____ _____   _____ _____    ___ \n|    \\|  _  |   | |  |  | |   __|   __|  |_  |\n|  |  |     | | | |    -|_|   __|   __|  |  _|\n|____/|__|__|_|___|__|__|_|__|  |__|     |___|\n\nx\n\n'
    x = clr(f"by sir.dank | {green}nuclearff.{green}com")
    cls(); print(align(clr(banner,4,colours=[white, white_normal, red, red_normal, red_dim]).replace('x',x)))

def open_workspace():
    
    dankff_path = os.path.join(os.environ['USERPROFILE'], 'Documents')
    if not os.path.exists(dankff_path):
        dankff_path = "C:\\"
    dankff_path = os.path.join(dankff_path, "dank.fusion-fall")
    if not os.path.exists(dankff_path): os.mkdir(dankff_path)
    os.chdir(dankff_path)
    
    banner()
    
    folders = [_ for _ in os.listdir() if os.path.isdir(_)]

    if len(folders) == 0:
        
        print(clr("\n  > No workspaces found!\n",2))
        while True:
            try:
                workspace = input(clr("  > New workspace name: ") + red)
                os.mkdir(workspace)
                os.chdir(workspace)
                break
            except:
                rm_line()
                print(clr(f"  > Failed to make directory: {workspace}",2))       
    
    else:
        
        print(clr("\n  - Workspaces:\n\n    0 > Create New Workspace"))
        for i, workspace in enumerate(folders):
            print(clr(f"    {i+1} > {workspace}"))
        
        print()
        while True:
            _ = input(clr("  > Select workspace [num/name]: ") + red)
            if _.isdigit() and int(_) >= 0 and int(_) <= len(folders):
                if int(_) == 0:
                    print()
                    while True:
                        try:
                            workspace = input(clr("  > New workspace name: ") + red)
                            if not os.path.isdir(workspace):
                                os.mkdir(workspace); break
                            else:
                                rm_line()
                        except:
                            rm_line()
                            print(clr(f"  > Failed to make directory: {workspace}",2))   
                    break
                else: workspace = folders[int(_)-1]; break
            elif _ in folders: workspace = _; break
            else: rm_line()
            
        os.chdir(workspace)
        workspace = os.getcwd()
        if "y" in input(clr("\n  > Open workspace in explorer? [y/n]: ") + red).lower():
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
            for dname, data in table.items():
                output[tname][dname] = data
        except: output[tname] = "<err>"
    
    if "CustomAssetBundle-TableData" in cab_name: file_name = "xdt1013.json"
    else: file_name = "xdt.json"

    json.dump(output, open(file_name, "w+"), indent=4)

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
        if "=" not in cmd: exec(f"print({to_exec})".replace('key', cmd))
        else: cmd = cmd.split(' = '); exec(to_exec.replace('key',cmd[0]) + f" = \"{cmd[1]}\"")
    elif mode == 2: 
        if len(cmd) == 1: exec(f"print({to_exec})".replace('key', cmd[0]))
        else: exec(to_exec.replace('key',cmd[0]) + f" = \"{cmd[1]}\"")
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
    
    for key in ['m_iDifficulty', 'm_iTeam', 'm_iNpcLevel', 'm_iNpcType', 'm_iHNpc', 'm_iHNpcNum', 'm_iNpcStyle', 'm_iAiType', 'm_iHP', 'm_iHPRegen', 'm_iDropType', 'm_iRegenTime', 'm_iHeight', 'm_iRadius', 'm_fScale', 'm_iPower', 'm_iAccuracy', 'm_iProtection', 'm_iDodge', 'm_iRunSpeed', 'm_iSwimSpeed', 'm_iJumpHeight', 'm_iJumpDistance', 'm_iSightRange', 'm_iIdleRange', 'm_iCombatRange', 'm_iAtkRange', 'm_iAtkAngle', 'm_iAtkRate', 'm_iEffectArea', 'm_iTargetMode', 'm_iTargetNumber', 'm_iInitalTime', 'm_iDeliverTime', 'm_iDelayTime', 'm_iDurationTime', 'm_iMegaType', 'm_iMegaTypeProb', 'm_iCorruptionType', 'm_iCorruptionTypeProb', 'm_iActiveSkill1', 'm_iActiveSkill1Prob', 'm_iActiveSkill2', 'm_iActiveSkill2Prob', 'm_iActiveSkill3', 'm_iActiveSkill3Prob', 'm_iSupportSkill', 'm_iPassiveBuff', 'm_iNeck', 'm_iTexture', 'm_iTexture2', 'm_iIcon1', 'm_iEffect', 'm_iSound', 'm_iWalkSpeed', 'm_iMapIcon', 'm_iLegStyle', 'm_iBarkerType', 'm_iMegaAni', 'm_iActiveSkill1Ani', 'm_iActiveSkill2Ani', 'm_iSupportSkillAni', 'm_iMegaString', 'm_iCorruptionString', 'm_iActiveSkill1String', 'm_iActiveSkill2String', 'm_iSupportSkillString', 'm_iServiceNumber']:
        while True:
            try: data[key] = int(input(clr(f"  > data['{key}'] (int) = ") + green)); break
            except: pass
            
    for key in ['m_fAnimationSpeed', 'm_fWalkAnimationSpeed', 'm_fRunAnimationSpeed']:
        while True:
            try: data[key] = float(input(clr(f"  > data['{key}'] (float) = ") + green)); break
            except: pass

    print(clr("  > xdtdata['m_pNpcTable']['m_pNpcData'].append(data)"))
    xdtdata['m_pNpcTable']['m_pNpcData'].append(data)

    #data = FFOrderedDict()
    #for key in ['m_iIconNumber', 'm_iIconType']:
    #    while True:
    #        try: data[key] = int(input(clr(f"  > data['{key}'] (int) = ") + green)); break
    #        except: pass
    #print(clr("  > xdtdata['m_pNpcTable']['m_pNpcIconData'].append(data)"))
    #xdtdata['m_pNpcTable']['m_pNpcIconData'].append(data)
    
    data = FFOrderedDict()
    for key in ['m_pstrMMeshModelString', 'm_pstrMTextureString', 'm_pstrMTextureString2', 'm_pstrFTextureString', 'm_pstrFTextureString2', 'm_pstrFMeshModelString']:
        while True:
            try: data[key] = input(clr(f"  > data['{key}'] (string) = ") + green); break
            except: pass
    print(clr("  > xdtdata['m_pNpcTable']['m_pNpcMeshData'].append(data)"))
    xdtdata['m_pNpcTable']['m_pNpcMeshData'].append(data)

    data = FFOrderedDict()
    for key in ['m_strName', 'm_strComment', 'm_strComment1', 'm_strComment2']:
        while True:
            try: data[key] = input(clr(f"  > data['{key}'] (string) = ") + green); break
            except: pass
    while True:
        try: data['m_iExtraNumber'] = int(input(clr(f"  > data['m_iExtraNumber'] (int) = ") + green)); break
        except: pass
    print(clr("  > xdtdata['m_pNpcTable']['m_pNpcBarkerData'].append(data)"))
    xdtdata['m_pNpcTable']['m_pNpcBarkerData'].append(data)
    
    data = FFOrderedDict()
    for key in ['m_strName', 'm_strComment', 'm_strComment1', 'm_strComment2']:
        while True:
            try: data[key] = input(clr(f"  > data['{key}'] (string) = ") + green); break
            except: pass
    while True:
        try: data['m_iExtraNumber'] = int(input(clr(f"  > data['m_iExtraNumber'] (int) = ") + green)); break
        except: pass
    print(clr("  > xdtdata['m_pNpcTable']['m_pNpcStringData'].append(data)"))
    xdtdata['m_pNpcTable']['m_pNpcStringData'].append(data)

def print_bundle():
    
    container = tabledata.objects[1].read()['m_Container']
    print(clr('asset\t\tindex\tsize\tpath'))
    for path, mtdt in container:
        print(clr('{}\t{}\t{}\t{}'.format(mtdt['asset'].path_id, mtdt['preloadIndex'], mtdt['preloadSize'], path)))

def print_content():
    
    print(clr('id\t\ttype_id\ttype\t\tname'))
    for id, obj in tabledata.objects.items():
        name = ''
        if hasattr(obj.read(), 'name'):
            name = obj.read().name
        try: print(clr('{}\t{}\t{}\t{}'.format(id, obj.type_id, obj.type, name)))
        except Exception as exc: print(clr('ERROR: ' + str(exc))) 

# main

def main():
    
    global tabledata, xdtdata, cab_name

    print(clr("  > Select Custom Asset Bundle..."))
    cab_path = ''
    while not cab_path:
        if "PYTHONHOME" in os.environ:
            cab_path = file_selector("Select Custom Asset Bundle", os.path.join(os.path.dirname(__file__), "dankware.ico")).replace('/','\\').replace('"','')
        else: #cab_path = input(clr("  > Drag and Drop Custom Asset Bundle: ")).replace('/','\\').replace('"','')
            cab_path = file_selector("Select Custom Asset Bundle").replace('/','\\').replace('"','')
    rm_line()
    
    print(clr(logger(f'  > cab_path = "{cab_path}"')))
    cab_name = str(cab_path.split('\\')[-1])
    print(clr(logger(f"  > tabledata = Asset.from_file(open('{cab_path}', 'rb'))")))
    tabledata = Asset.from_file(open(cab_path, 'rb'))
    
    tabledata_keys = [str(_) for _ in tabledata.objects.keys()]
    if input(clr(f"\n  > Print {len(tabledata.objects)} Available TableData Keys? [y/n]: ") + green).lower() == 'y':
        print(clr(logger("  > Available TableData Keys: \n\n" + '\n'.join(tabledata_keys) + "\n")))

    if "CustomAssetBundle-1dca92eecee4742d985b799d8226666d" in cab_name and "7" in tabledata_keys:
        print(clr("  > Suggested Key: 7"))
    elif "CustomAssetBundle-TableData" in cab_name and "2139558964" in tabledata_keys:
        print(clr("  > Suggested Key: 2139558964"))
    elif "CustomAssetBundle-8320bfa70e3f04727bfc405b1fd7efcc" in cab_name and "3" in tabledata_keys:
        print(clr("  > Suggested Key: 3"))
    elif "sharedassets0.assets" in cab_name and "1375" in tabledata_keys:
        print(clr("  > Suggested Key: 1375"))

    while True:    
        key = input(clr(f'  > TableData Key: ') + green)
        try:
            key = int(key)
            xdtdata = tabledata.objects[key].contents
            print(clr(logger(f"  > xdtdata = tabledata.objects[{key}].contents")))
            break
        except: print(clr(logger(f"  > Invalid Key: {key}"),2))
    print(clr("\n  > Pre-defined commands: print-bundle, print-content, dump-xdt, path_id('filename'), fix-bundles, add-npc, help, log, save, save-all, clear, exit\n"))
    
    help_msg = """  > Available Shortcuts With Examples:\n
 - aimport sound.wav, 22.5, sound  >  new_audio = tabledata.add_object(83); import_audio(new_audio.contents,'sound.wav',22.5,'sound'); tabledata.add2ab('sound.wav',new_audio.path_id)
 - aswap sound.wav, 22.5, sound  >  import_audio(xdtdata,'sound.wav',22.5,'sound')
 - export example.obj  >  open('example.obj','w').write(OBJMesh(xdtdata).export())
 - imesh npc_alienx.obj npc_alienx  >  import_mesh(xdtdata, 'npc_alienx.obj', 'npc_alienx')
 - key 0  >  xdtdata = tabledata.objects[0].contents
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
 - rename Cone02, DT_MTDB_ETC05  >  xdtdata.name = xdtdata.name.replace('Cone02','DT_MTDB_ETC05')
 - texture 344  >  print(xdtdata['m_pNpcTable']['m_pNpcMeshData'][344]['m_pstrMTextureString'])
 - texture 344 fusion_cheese  >  xdtdata['m_pNpcTable']['m_pNpcMeshData'][344]['m_pstrMTextureString'] = \"fusion_cheese\"
 - timport texture 1  >  new_texture = tabledata.add_object(28); import_texture(new_texture._contents,'texture.png','texture','dxt1'); tabledata.add2ab('texture.png',new_texture.path_id)
 - timport texture 5  >  new_texture = tabledata.add_object(28); import_texture(new_texture._contents,'texture.png','texture','dxt5'); tabledata.add2ab('texture.png',new_texture.path_id)
 - timport-mass 1  >  mass import_texture (fmt='dxt1')
 - timport-mass 5  >  mass import_texture (fmt='dxt5')
 - tswap texture.png texture 1  >  import_texture(xdtdata,'texture.png','texture','dxt1')
 - tswap texture.png texture 5  >  import_texture(xdtdata,'texture.png','texture','dxt5')
 - tswap-mass 1  >  mass import_texture (fmt='dxt1')
 - tswap-mass 5  >  mass import_texture (fmt='dxt5')"""

    while True:
        try:
            cmd = logger(input(f"  {red}> {green}"))
            print(reset, end='')
            cmd_lower = cmd.lower()

            if cmd_lower == "help": print(clr(help_msg))
            elif cmd_lower == "clear": cls()
            elif cmd_lower == "exit": break
            elif cmd_lower == "fix-bundles": fix_bundles()
            elif cmd_lower == "add-npc": add_npc()
            elif cmd_lower == "print-bundle": print_bundle()
            elif cmd_lower == "print-content": print_content()
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
                tabledata.add2ab(f"sound/{cmd[0]}",new_audio.path_id)

            elif cmd_lower.startswith('aswap '):
                cmd = cmd.replace('aswap ','').split(', ')
                import_audio(xdtdata, cmd[0], int(cmd[1]), cmd[2])

            elif cmd_lower.startswith('export '):
                cmd = cmd.replace('export ','').replace(' ','')
                open(cmd,'w').write(OBJMesh(xdtdata).export())

            elif cmd_lower.startswith('imesh '):
                cmd = cmd.replace('imesh ','').split(' ')
                import_mesh(xdtdata, cmd[0], cmd[1])
                
            elif cmd_lower.startswith('key '):
                key = int(cmd.replace('key ',''))
                xdtdata = tabledata.objects[key].contents

            elif cmd_lower.startswith('ms-info '):
                print(xdtdata['m_pMissionTable']['m_pMissionData'][int(cmd.replace('ms-info ',''))])

            elif cmd_lower.startswith('ms-npc '):
                cmd = cmd.replace('ms-npc ','').split(' ')
                to_exec = "xdtdata['m_pMissionTable']['m_pMissionData'][key]['m_iHNPCID']"
                shortcut(2, cmd, to_exec)

            elif cmd_lower.startswith('ms-string '):
                cmd = cmd.replace('ms-string ','')
                to_exec = "xdtdata['m_pMissionTable']['m_pMissionStringData'][key]"
                shortcut(1, cmd, to_exec)

            elif cmd_lower.startswith('ms-task '):
                cmd = cmd.replace('ms-task ','').split(' ')
                to_exec = "xdtdata['m_pMissionTable']['m_pMissionData'][key]['m_iHTaskID']"
                shortcut(2, cmd, to_exec)

            elif cmd_lower.startswith('ms-tasknext '):
                cmd = cmd.replace('ms-tasknext ','').split(' ')
                to_exec = "xdtdata['m_pMissionTable']['m_pMissionData'][key]['m_iSUOutgoingTask']"
                shortcut(2, cmd, to_exec)

            elif cmd_lower.startswith('mesh '):
                cmd = cmd.replace('mesh ','').split(' ')
                to_exec = "xdtdata['m_pNpcTable']['m_pNpcMeshData'][key]['m_pstrMMeshModelString']"
                shortcut(2, cmd, to_exec)

            elif cmd_lower.startswith('meshid '):
                cmd = cmd.replace('meshid ','').split(' ')
                to_exec = "xdtdata['m_pNpcTable']['m_pNpcData'][key]['m_iMesh']"
                shortcut(2, cmd, to_exec)

            elif cmd_lower.startswith('npc-name '):
                cmd = cmd.replace('npc-name ','')
                to_exec = "xdtdata['m_pNpcTable']['m_pNpcStringData'][key]['m_strName']"
                shortcut(1, cmd, to_exec)

            elif cmd_lower.startswith('objects '):
                cmd = cmd.replace('objects ','').split(' ')
                to_exec = f"for _ in range({cmd[0]},{cmd[1]}): print(f'{{_}} - {{tabledata.objects[_].contents}}')"
                exec(to_exec); print()
            
            elif cmd_lower.startswith('rename '):
                cmd = cmd.replace('rename ','').split(', ')
                to_exec = f"xdtdata.name = xdtdata.name.replace('{cmd[0]}','{cmd[1]}')"
                exec(to_exec); print()

            elif cmd_lower.startswith('texture '):
                cmd = cmd.replace('texture ','').split(' ')
                to_exec = "xdtdata['m_pNpcTable']['m_pNpcMeshData'][key]['m_pstrMTextureString']"
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
                exec(cmd)
            
            print()

        except: print(clr(err(sys.exc_info()) + '\n', 2))

def menu():
    
    sys.setrecursionlimit(10000)
    open_workspace()
    
    while True:
        
        banner(); print(clr(f"\n  1 > CAB Explorer / Editor\n  2 > Fix Bundles\n  3 > Mission Builder (coming soon)\n  4 > Change workspace [{os.path.basename(os.getcwd())}]\n  5 > Visit {green}nuclearff.{green}com{white}\n  6 > Exit\n"))
        
        choice = input(clr("  > Choice: ") + green)
        if choice == "1": banner(); main()
        elif choice == "2": banner(); fix_bundles()
        #elif choice == "3": banner(); mission_builder()
        elif choice == "4": open_workspace()
        elif choice == "5": os.system(f'start https://nuclearff.com/')
        elif choice == "6": break
        else: rm_line()

if __name__ == '__main__':

    log = ''
    
    if magickwand_installed:
        menu()
    else:
        print(clr("\n  > Please install ImageMagick and then run the module!\n",2))
        input(clr("  > Press [ENTER] to exit..."))
        
    for _ in ['log', 'tabledata', 'xdtdata', 'cab_name', 'setup', 'banner', 'open_workspace', 'logger', 'path_id', 'dump_xdt', 'fix_bundles', 'tswap_mass', 'timport_mass', 'shortcut', 'add_npc', 'main', 'menu']:
        try: del globals()[_]
        except: pass
