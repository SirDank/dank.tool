import os
from ursina import *
from dankware import cls, clr
from numpy.random import choice, randint
from ursina.scripts.smooth_follow import SmoothFollow
from ursina.prefabs.first_person_controller import FirstPersonController

cls()

try:
    os.environ['DANK_TOOL_VERSION']
except:
    os.chdir(os.path.dirname(__file__))
    # this does not work for some reason!
    #os.chdir("..")
    #os.chdir("ursina")
    #application.package_folder = os.getcwd()
    #application.asset_folder = os.path.join(os.getcwd(), "ursina")

input(clr("""\n  [ DISCLAIMER ]

  - This game is in early development, expect bugs!
  - The error reporting system does not support this game, please report bugs manually!
  - If the ground is not visible, restart the game!
  - You might need to use max brightness!
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
player = FirstPersonController(speed=2.5)
player_camera = Entity(parent=camera, position=(0.5, -0.5, 0.8), rotation=(0, 135, 5))
sky = Sky(texture='sky.png')

world_size = 250 # n*2 x n*2
render_dist = 15 # n*2 x n*2
collision_dist = 2 # n*2 x n*2
tree_heights = 10
tree_heights = list(range(tree_heights - 3, tree_heights + 4))
textures = {
    load_texture("grass1"): 0.445,
    load_texture("grass2"): 0.445,
    load_texture("mossy_cobblestone1"): 0.05,
    load_texture("mossy_cobblestone2"): 0.05,
    load_texture("mossy_stone_bricks"): 0.01,
}
weights = tuple(textures.values())
textures = tuple(textures)
tree_log = load_texture("acacia_log")
tree_leaves = load_texture("azalea_leaves")
leaves = tuple([
    load_texture("mangrove_leaves_inventory"),
    load_texture("azalea_leaves"),
    load_texture("flowering_azalea_leaves")
])

# lighting

def enable_lighting():

    scene.fog_density = 0.2
    scene.fog_color = color.black
    torch = Entity(model="flashlight.gltf", scale=0.3)
    torch_light = SpotLight(parent=torch, color=color.white, position=(3, 0.5, 4.2), rotation=(0, -135, -5)) # noqa: F841
    torch.add_script(SmoothFollow(target=player_camera, rotation_speed=10))

enable_lighting()

# terrain vertices generation

start_time = time.time()
print(clr("\n  > Generating terrain vertices..."))

def generate_vertices(x, z):

    new_vertices = [Vec3(x-.5, 0, z-.5), Vec3(x+.5, 0, z-.5), Vec3(x+.5, 0, z+.5), Vec3(x-.5, 0, z+.5)]

    terrain_beside = bool((x-1, z) in terrain)
    terrain_below = bool((x, z-1) in terrain)

    if terrain_below and terrain_beside:
        vert_0_y = terrain[(x, z-1)]['vertices'][3][1]
        vert_1_y = terrain[(x, z-1)]['vertices'][2][1]
        vert_3_y = terrain[(x-1, z)]['vertices'][2][1]
        avg = (vert_0_y + vert_1_y + vert_3_y)/3
        vert_2_y = choice([avg, avg+.1, avg+.2, avg-.1, avg-.2]) #choice([vert_0_y, vert_0_y+.05, vert_0_y-.05, vert_1_y, vert_1_y+.05, vert_1_y-.05, vert_3_y, vert_3_y+.05, vert_3_y-.05])
        new_vertices[0][1] = vert_0_y
        new_vertices[1][1] = vert_1_y
        new_vertices[2][1] = vert_2_y
        new_vertices[3][1] = vert_3_y

    elif terrain_beside:
        vert_0_y = terrain[(x-1, z)]['vertices'][1][1]
        vert_3_y = terrain[(x-1, z)]['vertices'][2][1]
        avg = (vert_0_y + vert_3_y)/2
        vert_1_y = choice([avg, avg+.1, avg+.2, avg-.1, avg-.2]) #choice([vert_0_y, vert_0_y+.05, vert_0_y-.05, vert_3_y, vert_3_y+.05, vert_3_y-.05])
        avg = (vert_0_y + vert_1_y + vert_3_y)/3
        vert_2_y = choice([avg, avg+.1, avg+.2, avg-.1, avg-.2]) #choice([vert_0_y, vert_0_y+.05, vert_0_y-.05, vert_3_y, vert_3_y+.05, vert_3_y-.05])
        new_vertices[0][1] = vert_0_y
        new_vertices[1][1] = vert_1_y
        new_vertices[2][1] = vert_2_y
        new_vertices[3][1] = vert_3_y

    elif terrain_below:
        vert_0_y = terrain[(x, z-1)]['vertices'][3][1]
        vert_1_y = terrain[(x, z-1)]['vertices'][2][1]
        avg = (vert_0_y + vert_1_y)/2
        vert_2_y = choice([avg, avg+.1, avg+.2, avg-.1, avg-.2]) #choice([vert_0_y, vert_0_y+.05, vert_0_y-.05, vert_1_y, vert_1_y+.05, vert_1_y-.05])
        avg = (vert_0_y + vert_1_y + vert_2_y)/3
        vert_3_y = choice([avg, avg+.1, avg+.2, avg-.1, avg-.2]) #choice([vert_0_y, vert_0_y+.05, vert_0_y-.05, vert_1_y, vert_1_y+.05, vert_1_y-.05])
        new_vertices[0][1] = vert_0_y
        new_vertices[1][1] = vert_1_y
        new_vertices[2][1] = vert_2_y
        new_vertices[3][1] = vert_3_y

    else:
        new_vertices[0][1] = choice([0, .1, .2, -.1, -.2])
        new_vertices[1][1] = choice([0, .1, .2, -.1, -.2])
        new_vertices[2][1] = choice([0, .1, .2, -.1, -.2])
        new_vertices[3][1] = choice([0, .1, .2, -.1, -.2])

    global lowest_y, highest_y
    lowest_y = min(lowest_y, new_vertices[0][1], new_vertices[1][1], new_vertices[2][1], new_vertices[3][1]) # pylint: disable=used-before-assignment
    highest_y = max(highest_y, new_vertices[0][1], new_vertices[1][1], new_vertices[2][1], new_vertices[3][1]) # pylint: disable=used-before-assignment

    return new_vertices

lowest_y = 0
highest_y = 0
terrain = {}

for x in range(-world_size, world_size+1):
    for z in range(-world_size, world_size+1):
        terrain[(x, z)] = {}
        terrain[(x, z)]['entities'] = None
        terrain[(x, z)]['vertices'] = generate_vertices(x, z)
del generate_vertices

lowest_y -= 10
highest_y += 10
triangles = [0,1,2,0,2,3]
uvs = [(0,0),(1,0),(1,1),(0,1)]

print(clr(f"\n  > Generated {len(terrain)} sets of terrain vertices in {int(time.time() - start_time)} seconds!\n"))
del start_time

# randomised entity generation

def create_entity(pos, vertices):

    terrain[pos]['entities'] = []

    mesh = Mesh(vertices=vertices, triangles=triangles, uvs=uvs)
    mesh.generate_normals(smooth=True)
    entity = Entity(model=mesh, collider="mesh", texture=choice(textures, p=weights), ignore=True)
    entity.collision = False
    terrain[pos]['entities'].append(entity)

    if choice([0, 1], p=[0.99, 0.01]):

        _vertices = vertices.copy()
        _vertices[0][1] += 0.01
        _vertices[1][1] += 0.01
        _vertices[2][1] += 0.01
        _vertices[3][1] += 0.01

        mesh = Mesh(vertices=_vertices, triangles=triangles, uvs=uvs)
        mesh.generate_normals(smooth=True)
        entity = Entity(model=mesh, collider="mesh", texture=choice(leaves), ignore=True)
        entity.collision = False
        terrain[pos]['entities'].append(entity)

    elif choice([0, 1], p=[0.98, 0.02]):

        y_rot = randint(0, 90)
        x_rot = randint(-5, +5)
        z_rot = randint(-5, +5)
        tree_height = choice(tree_heights)
        leaves_level_start = tree_height-3
        leaves_level_current = 1
        next_pos = Vec3(pos[0], min(vertices[0][1], vertices[1][1], vertices[2][1], vertices[3][1]), pos[1])

        for _ in range(tree_height):

            entity = Entity(model="cube", collider="box", texture=tree_log, position=next_pos, rotation=(x_rot,y_rot,z_rot), ignore=True)
            entity.collision = False
            terrain[pos]['entities'].append(entity)

            if _ > leaves_level_start:

                match leaves_level_current:
                    case 1:
                        back_2 = entity.back + entity.back
                        forward_2 = entity.forward + entity.forward
                        left_2 = entity.left + entity.left
                        right_2 = entity.right + entity.right

                        for _pos in [entity.back + left_2, left_2, entity.forward + left_2, back_2 + entity.left, forward_2 + entity.left, back_2, forward_2, back_2 + entity.right, forward_2 + entity.right, entity.back + right_2, right_2, entity.forward + right_2]:
                            entity = Entity(model="cube", texture=tree_leaves, position=next_pos + _pos, rotation=(x_rot,y_rot,z_rot), ignore=True)
                            entity.collision = False
                            terrain[pos]['entities'].append(entity)

                    case 2:
                        for _pos in [entity.back + entity.left, entity.left, entity.forward + entity.left, entity.back, entity.forward, entity.back + entity.right, entity.right, entity.forward + entity.right]:
                            entity = Entity(model="cube", texture=tree_leaves, position=next_pos + _pos, rotation=(x_rot,y_rot,z_rot), ignore=True)
                            entity.collision = False
                            terrain[pos]['entities'].append(entity)

                leaves_level_current += 1

            y_rot = randint(y_rot-5, y_rot+5)
            x_rot = randint(x_rot-5, x_rot+5)
            z_rot = randint(z_rot-5, z_rot+5)
            next_pos += entity.up

# load / unload entities

def first_load():

    for x in range(int(player.x) - render_dist, int(player.x) + render_dist + 1):
        for z in range(int(player.z) - render_dist, int(player.z) + render_dist + 1):
            pos = (x, z)
            if pos not in rendered_chunks and pos in terrain:
                if not terrain[pos]['entities']:
                    create_entity(pos, terrain[pos]['vertices'])
                else:
                    for entity in terrain[pos]['entities']:
                        entity.enabled = True
                rendered_chunks[pos] = None
            render_grid[pos] = None

    for x in range(int(player.x) - collision_dist, int(player.x) + collision_dist + 1):
        for z in range(int(player.z) - collision_dist, int(player.z) + collision_dist + 1):
            pos = (x, z)
            if pos in rendered_chunks:
                for entity in terrain[pos]['entities']:
                    entity.collision = True
            collision_grid[pos] = None

def reset_render_grid():

    global render_grid

    _render_grid = {}
    for x in range(int(player.x) - render_dist, int(player.x) + render_dist + 1):
        for z in range(int(player.z) - render_dist, int(player.z) + render_dist + 1):
            pos = (x, z)
            render_grid[pos] = None
            _render_grid[pos] = None
            if pos not in r_loop and pos not in rendered_chunks and pos in terrain:
                r_loop.append(pos)
    render_grid = _render_grid.copy()

def reset_collision_grid():

    global collision_grid

    _collision_grid = {}
    for x in range(int(player.x) - collision_dist, int(player.x) + collision_dist + 1):
        for z in range(int(player.z) - collision_dist, int(player.z) + collision_dist + 1):
            pos = (x, z)
            _collision_grid[pos] = None
            if pos not in collision_grid and pos in rendered_chunks:
                collision_grid[pos] = None
                c_loop.append(pos)
    collision_grid = _collision_grid.copy()

def render_loop():

    try:
        pos = r_loop.pop(0)
        if not terrain[pos]['entities']:
            create_entity(pos, terrain[pos]['vertices'])
        else:
            for entity in terrain[pos]['entities']:
                entity.enabled = True
        rendered_chunks[pos] = None
    except IndexError:
        pass

def collision_loop():

    try:
        pos = c_loop.pop(0)
        for entity in terrain[pos]['entities']:
            entity.collision = True
    except IndexError:
        pass

def unload():

    to_delete = []

    for pos in rendered_chunks:
        if pos not in render_grid:
            for entity in terrain[pos]['entities']:
                _ = destroy(entity)
            terrain[pos]['entities'] = None
            to_delete.append(pos)
        elif pos not in collision_grid:
            for entity in terrain[pos]['entities']:
                entity.collision = False

    for pos in to_delete:
        del rendered_chunks[pos]

# other stuff

def check_player_y():
    if player.y < lowest_y:
        player.position = (0, highest_y, 0)

def input(key): # pylint: disable=function-redefined
    if key == 'escape':
        if "DANK_TOOL_VERSION" in os.environ:
            os.system("taskkill /f /im dank.tool.exe")
        else:
            application.quit()

r_loop = []
render_grid = {}
rendered_chunks = {}

c_loop = []
collision_grid = {}

ambiance_trees = Audio("ambiance_trees.m4a", loop=True, autoplay=True, volume=1)
ambiance_crickets = Audio("ambiance_crickets.m4a", loop=True, autoplay=True, volume=0.3)

player.position = (0, 100, 0)

first_load()

sequence_1 = Sequence(Func(check_player_y), Wait(1), loop=True)

sequence_2 = Sequence(Func(reset_render_grid), Wait(0.25), loop=True)
sequence_3 = Sequence(Func(render_loop), Wait(0.005), loop=True)

sequence_4 = Sequence(Func(reset_collision_grid), Wait(0.25), loop=True)
sequence_5 = Sequence(Func(collision_loop), Wait(0.05), loop=True)

sequence_6 = Sequence(Func(unload), Wait(1), loop=True)

sequence_1.start()
sequence_2.start()
sequence_3.start()
sequence_4.start()
sequence_5.start()
sequence_6.start()

app.run()
