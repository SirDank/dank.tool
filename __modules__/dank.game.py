import os
from ursina import *
from dankware import cls, clr, title
from numpy.random import choice, randint
from ursina.shaders import texture_blend_shader
from concurrent.futures import ThreadPoolExecutor
from ursina.prefabs.first_person_controller import FirstPersonController

cls()
title("𝚍𝚊𝚗𝚔.𝚐𝚊𝚖𝚎")

try:
    os.environ['DANK_TOOL_VERSION']
except:
    os.chdir(os.path.dirname(__file__))
    os.chdir("..")
    #os.chdir("ursina")
    #application.package_folder = os.getcwd()
    # this does not work for some reason!
    application.asset_folder = os.path.join(os.getcwd(), "ursina")

input(clr("""\n  [ DISCLAIMER ]

  - This game is in early development, expect bugs!
  - Game updates might be slow!
  - Built with Ursina Engine!

  [ CONTROLS ]
  
  - WASD to move
  - SPACE to jump
  - ESC to quit (will not return to menu)
  
  > Press [ENTER] to start... 
"""))

# game settings

app = Ursina(
    title='𝚍𝚊𝚗𝚔.𝚐𝚊𝚖𝚎',
    borderless=False,
    fullscreen=True,
    vsync=True,
    development_mode=False,
    #show_ursina_splash=True
)

#player = EditorCamera()
player = FirstPersonController()
sky = Sky(texture='sky.png')
Entity.default_shader = texture_blend_shader

world_size = 250 # n*2 x n*2
render_dist = 10 # nxn
textures = {
    "grass1": 0.445,
    "grass2": 0.445,
    "mossy_cobblestone1": 0.05,
    "mossy_cobblestone2": 0.05,
    "mossy_stone_bricks": 0.01,
}
weights = tuple(textures.values())
textures = tuple(textures.keys())

# lighting

def enable_lighting():
    scene.fog_density = 0.3
    scene.fog_color = color.black
    player_light = PointLight(color=color.white, parent=player, position=(0, 2, 0))

enable_lighting()

# terrain vertices generation

start_time = time.time()
print(clr("\n  > Generating terrain vertices..."))

def gen_vertices(x, z):
    
    global lowest_y, highest_y
    
    new_vertices = [Vec3(x-.5, 0, z-.5), Vec3(x+.5, 0, z-.5), Vec3(x+.5, 0, z+.5), Vec3(x-.5, 0, z+.5)]

    terrain_keys = terrain.keys()
    if (x-1, z) in terrain_keys: terrain_beside = True
    else: terrain_beside = False
    if (x, z-1) in terrain_keys: terrain_below = True
    else: terrain_below = False
        
    if terrain_below and terrain_beside:
        vert_0_y = terrain[(x, z-1)][3][1]
        vert_1_y = terrain[(x, z-1)][2][1]
        vert_3_y = terrain[(x-1, z)][2][1]
        vert_2_y = choice([vert_0_y, vert_0_y+.05, vert_0_y-.05, vert_1_y, vert_1_y+.05, vert_1_y-.05, vert_3_y, vert_3_y+.05, vert_3_y-.05])
        new_vertices[0][1] = vert_0_y
        new_vertices[1][1] = vert_1_y
        new_vertices[2][1] = vert_2_y
        new_vertices[3][1] = vert_3_y
    
    elif terrain_beside:
        vert_0_y = terrain[(x-1, z)][1][1]
        vert_3_y = terrain[(x-1, z)][2][1]
        vert_1_y = choice([vert_0_y, vert_0_y+.05, vert_0_y-.05, vert_3_y, vert_3_y+.05, vert_3_y-.05])
        vert_2_y = choice([vert_0_y, vert_0_y+.05, vert_0_y-.05, vert_3_y, vert_3_y+.05, vert_3_y-.05])
        new_vertices[0][1] = vert_0_y
        new_vertices[1][1] = vert_1_y
        new_vertices[2][1] = vert_2_y
        new_vertices[3][1] = vert_3_y

    elif terrain_below:
        vert_0_y = terrain[(x, z-1)][3][1]
        vert_1_y = terrain[(x, z-1)][2][1]
        vert_2_y = choice([vert_0_y, vert_0_y+.05, vert_0_y-.05, vert_1_y, vert_1_y+.05, vert_1_y-.05])
        vert_3_y = choice([vert_0_y, vert_0_y+.05, vert_0_y-.05, vert_1_y, vert_1_y+.05, vert_1_y-.05])
        new_vertices[0][1] = vert_0_y
        new_vertices[1][1] = vert_1_y
        new_vertices[2][1] = vert_2_y
        new_vertices[3][1] = vert_3_y
        
    lowest_y = min(lowest_y, new_vertices[0][1], new_vertices[1][1], new_vertices[2][1], new_vertices[3][1])
    highest_y = max(highest_y, new_vertices[0][1], new_vertices[1][1], new_vertices[2][1], new_vertices[3][1])

    return tuple(new_vertices)

lowest_y = 0
highest_y = 0
terrain = {}
for x in range(-world_size, world_size):
    for z in range(-world_size, world_size):
        terrain[(x, z)] = gen_vertices(x, z)
del gen_vertices
lowest_y -= 10
highest_y += 10
terrain_backup = terrain.copy()
terrain_keys = terrain.keys()
triangles = [(0,1,2,3)]
uvs = [(0,0),(1,0),(1,1),(0,1)]

print(clr(f"\n  > Generated {len(terrain_keys)} sets of terrain vertices in {int(time.time() - start_time)} seconds!\n"))
del start_time

# randomised entity generation

def create_entity(x, z, vertices):

    pos = (x, z)
    terrain[pos] = []
    
    mesh = Mesh(vertices=vertices, triangles=triangles, uvs=uvs)
    mesh.generate_normals(smooth=True)
    entity = Entity(model=mesh, collider="mesh", texture=choice(textures, p=weights), ignore=True)
    entity.collision = False
    terrain[pos].append(entity)
    
    if choice([0, 1], p=[0.99, 0.01]):
        
        vertices[0][1] += 0.01
        vertices[1][1] += 0.01
        vertices[2][1] += 0.01
        vertices[3][1] += 0.01
        
        mesh = Mesh(vertices=vertices, triangles=triangles, uvs=uvs)
        mesh.generate_normals(smooth=True)
        entity = Entity(model=mesh, collider="mesh", texture=choice(["mangrove_leaves_inventory", "azalea_leaves", "flowering_azalea_leaves"]), ignore=True)
        entity.collision = False
        terrain[pos].append(entity)
    
    if choice([0, 1], p=[0.98, 0.02]):
       
        y_rot = randint(0, 90)
        x_rot = randint(-5, +5)
        z_rot = randint(-5, +5)
        leaves_level_current = 1
        leaves_level_start = (render_dist)-3
        next_pos = Vec3(x, min(vertices[0][1], vertices[1][1], vertices[2][1], vertices[3][1]), z)

        for _ in range(render_dist):
            
            entity = Entity(model="cube", collider="box", texture="acacia_log", position=next_pos, rotation=(x_rot,y_rot,z_rot), ignore=True)
            entity.collision = False
            terrain[pos].append(entity)
            
            if _ > leaves_level_start:

                back_2 = entity.back + entity.back
                forward_2 = entity.forward + entity.forward
                left_2 = entity.left + entity.left
                right_2 = entity.right + entity.right

                if leaves_level_current == 1:
                    # [back_2 + left_2, entity.back + left_2, left_2, entity.forward + left_2, forward_2 + left_2, back_2 + entity.left, forward_2 + entity.left, back_2, forward_2, back_2 + entity.right, forward_2 + entity.right, back_2 + right_2, entity.back + right_2, right_2, entity.forward + right_2, forward_2 + right_2]
                    for _pos in [entity.back + left_2, left_2, entity.forward + left_2, back_2 + entity.left, forward_2 + entity.left, back_2, forward_2, back_2 + entity.right, forward_2 + entity.right, entity.back + right_2, right_2, entity.forward + right_2]:
                        entity = Entity(model="cube", texture="azalea_leaves", position=next_pos + _pos, rotation=(x_rot,y_rot,z_rot), ignore=True)
                        entity.collision = False
                        terrain[pos].append(entity)
                if leaves_level_current == 2:
                    for _pos in [entity.back + entity.left, entity.left, entity.forward + entity.left, entity.back, entity.forward, entity.back + entity.right, entity.right, entity.forward + entity.right]:
                        entity = Entity(model="cube", texture="azalea_leaves", position=next_pos + _pos, rotation=(x_rot,y_rot,z_rot), ignore=True)
                        entity.collision = False
                        terrain[pos].append(entity)
                
                leaves_level_current += 1
                    
            y_rot = randint(y_rot-5, y_rot+5)
            x_rot = randint(x_rot-5, x_rot+5)
            z_rot = randint(z_rot-5, z_rot+5)
            next_pos += entity.up

def check_player_pos():
    while running:
        if player.y < lowest_y:
            player.position = (0, highest_y, 0)
        time.sleep(1)

# load / unload entities

def load_and_unload():

    rendered_chunks = {}
    r_lower_limit = render_dist
    r_upper_limit = render_dist + 1

    collision_dist = 2
    c_lower_limit = collision_dist
    c_upper_limit = collision_dist + 1

    while running:

        render_grid = {}
        for x in range(int(player.x) - r_lower_limit, int(player.x) + r_upper_limit):
            for z in range(int(player.z) - r_lower_limit, int(player.z) + r_upper_limit):
                pos = (x, z)
                if not pos in rendered_chunks.keys() and pos in terrain_keys:
                    if type(terrain[pos]) == tuple:
                        create_entity(x, z, terrain[pos])
                    else:
                        for entity in terrain[pos]:
                            entity.enabled = True
                    rendered_chunks[pos] = ''
                render_grid[pos] = ''
        
        collision_grid = {}
        for x in range(int(player.x) - c_lower_limit, int(player.x) + c_upper_limit):
            for z in range(int(player.z) - c_lower_limit, int(player.z) + c_upper_limit):
                pos = (x, z)
                if pos in rendered_chunks.keys():
                    for entity in terrain[pos]:
                        entity.collision = True
                collision_grid[pos] = ''
        
        for pos in [_ for _ in rendered_chunks.keys()]:
            if not pos in collision_grid.keys():
                for entity in terrain[pos]:
                    entity.collision = False
            if not pos in render_grid.keys():
                for _ in range(len(terrain[pos])):
                    #terrain[pos][_].enabled = False
                    terrain[pos][_] = destroy(terrain[pos][_])
                terrain[pos] = terrain_backup[pos]
                del rendered_chunks[pos]
        
        time.sleep(0.1)

def input(key):
    if key == 'escape':
        global running
        running = False
        executor.shutdown(wait=True, cancel_futures=True)
        try:
            os.environ['DANK_TOOL_VERSION']
            os.system("taskkill /f /im dank.tool.exe")
        except:
            application.quit()

running = True
player.position = (0, 20, 0)
executor = ThreadPoolExecutor(max_workers=5)
executor.submit(check_player_pos)
executor.submit(load_and_unload)
app.run()