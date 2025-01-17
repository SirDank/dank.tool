import os
import pretty_errors
from ursina import *
from dankware import cls, clr
from numpy.random import randint
from numpy.random import choice as randchoice
from ursina.scripts.smooth_follow import SmoothFollow
from ursina.prefabs.first_person_controller import FirstPersonController

cls()

if 'DANK_TOOL_VERSION' not in os.environ:
    os.chdir(os.path.dirname(__file__))
    # this does not work for some reason!
    #os.chdir("..")
    #os.chdir("ursina")
    #application.package_folder = os.getcwd()
    #application.asset_folder = os.path.join(os.getcwd(), "ursina")

input(clr("""\n  [ DISCLAIMER ]

  - This game is in early development, expect bugs!
  - If the ground is not visible, restart the game!
  - You might need to use max brightness!
  - Game updates might be slow!
  - Built with Ursina Engine!

  [ CONTROLS ]
  
  - WASD to move
  - SPACE to jump
  - ESC to pause / quit game
  
  > Press [ENTER] to start... 
"""))

# game settings

app = Ursina(
    title='𝚍𝚊𝚗𝚔.𝚐𝚊𝚖𝚎',
    icon = (os.path.join(os.path.dirname(__file__), "dankware.ico") if 'DANK_TOOL_VERSION' in os.environ else 'textures/ursina.ico'),
    borderless=False,
    fullscreen=True,
    development_mode=False,
    show_ursina_splash=True,
)

# player = EditorCamera()
player = FirstPersonController(speed=2.5)
player_camera = Entity(parent=camera, position=(0.5, -0.5, 0.8), rotation=(0, 135, 5))
sky = Sky(texture='sky.png')

settings = {
    'world_size': 250, # n*2 x n*2
    'render_dist': 15, # n*2 x n*2
    'collision_dist': 2, # n*2 x n*2
    'tree_heights': list(range(7, 14)),
}

textures = {
    load_texture("grass1"): 0.445,
    load_texture("grass2"): 0.445,
    load_texture("mossy_cobblestone1"): 0.05,
    load_texture("mossy_cobblestone2"): 0.05,
    load_texture("mossy_stone_bricks"): 0.01,
}

weights = tuple(textures.values())
textures = tuple(textures)
tree_log_texture = load_texture("acacia_log")
tree_leaves_texture = load_texture("azalea_leaves")
leaves_textures = tuple([
    load_texture("mangrove_leaves_inventory"),
    load_texture("azalea_leaves"),
    load_texture("flowering_azalea_leaves")
])

# custom camera shader

player_stress = {
    'min': 0.0,
    'max': 0.1,
    'current': 0.0,
    'speed': 0.000025, # final
    # 'speed': 0.00025, # fast
    'direction': 1,
    'index': 0,
    'levels': [],
}

while player_stress['current'] <= player_stress['max']:
    player_stress['levels'].append(player_stress['current'])
    player_stress['current'] += player_stress['speed']
player_stress['current'] = player_stress['min']
# linear to ease-in
player_stress['levels'] = tuple(player_stress['levels'][-1] * (x / player_stress['levels'][-1])**25 for x in player_stress['levels'])
player_stress['index_max'] = len(player_stress['levels'])
del player_stress['current'], player_stress['speed']

camera_blur_noise_shader = Shader(
    name='camera_blur_noise_shader',
    fragment='''
    #version 430

    uniform sampler2D tex;
    in vec2 uv;
    uniform float blur_size;
    uniform float noise_offset;
    uniform float noise_strength;
    out vec4 color;

    // Function to apply vertical blur
    vec4 apply_vertical_blur(vec2 uv) {
        vec4 col = vec4(0.0);
        for(float i = 0.0; i < 10.0; i++) {
            vec2 offset_uv = uv + vec2(0.0, (i / 9.0 - 0.5) * blur_size);
            col += texture(tex, offset_uv);
        }
        col /= 10.0;
        return col;
    }

    // Function to apply noise
    vec3 apply_noise(vec3 rgb, vec2 uv) {
        float noise = fract(sin(dot(uv + noise_offset, vec2(12.9898, 78.233))) * 43758.5453);
        noise = (noise - 0.5) * noise_strength;
        rgb += noise;
        return rgb;
    }

    void main() {
        vec4 blurred_color = apply_vertical_blur(uv);
        vec3 noisy_color = apply_noise(blurred_color.rgb, uv);
        color = vec4(noisy_color, 1.0);
    }
    ''',
    default_input={
        'blur_size': player_stress['min'],
        'noise_offset': 1.0,
        'noise_strength': player_stress['min'],
    }
)

# pause menu

class PauseMenu(Entity):
    def __init__(self):
        super().__init__()
        self.pause_menu = Entity(parent=camera.ui, enabled=False)

        # if application.development_mode:
        self.render_mode_text = Text(text='Render Mode: default', parent=self.pause_menu, position=(0, 0.1875), origin=(0, 0))
        self.render_mode_buttons = []
        for i, mode in enumerate(window.render_modes):
            button = Button(text=mode.capitalize(), parent=self.pause_menu, scale=(0.15, 0.05), position=(i * 0.16 - ((len(window.render_modes) * (0.16 - (len(window.render_modes)*0.01)))/2), 0.1125), color=color.black, radius=0.25)
            button.on_click = Func(self.change_render_mode, mode)
            self.render_mode_buttons.append(button)

        self.camera_mode_text = Text(text='Camera Mode: None', parent=self.pause_menu, position=(0, -0.1125), origin=(0, 0))
        self.camera_mode_buttons = []
        for i, mode in enumerate(['Blur Noise', 'None']):
            button = Button(text=mode, parent=self.pause_menu, scale=(0.15, 0.05), position=(i * 0.16 - ((2 * (0.16 - (2*0.01)))/2), -0.1875), color=color.black, radius=0.25)
            button.on_click = Func(self.change_camera_mode, mode)
            self.camera_mode_buttons.append(button)

        if not application.development_mode:
            self.render_mode_text.disable()
            self.camera_mode_text.disable()
            for button in (self.render_mode_buttons + self.camera_mode_buttons):
                button.disable()

        self.resume_button = Button(text='Resume', parent=self.pause_menu, scale=(0.15, 0.05), position=(0, 0.0375), color=color.green, radius=0.25)
        self.quit_button = Button(text='Quit', parent=self.pause_menu, scale=(0.15, 0.05), position=(0, -0.0375), color=color.red, radius=0.25)
        self.resume_button.on_click = self.resume_game
        self.quit_button.on_click = self.quit_game

    def pause_game(self):
        self.pause_menu.enabled = True
        application.paused = True
        mouse.visible = True
        player.disable()
        time.dt = 0

    def resume_game(self):
        self.pause_menu.enabled = False
        application.paused = False
        mouse.visible = False
        player.enable()
        time.dt = 1

    def quit_game(self):
        if "DANK_TOOL_VERSION" in os.environ:
            os.system("taskkill /f /im dank.tool.exe")
        else:
            application.quit()

    def change_render_mode(self, mode):
        if window.render_mode != mode:
            self.render_mode_text.text = f'Render Mode: {mode}'
            window.render_mode = mode

    def change_camera_mode(self, mode):
        if self.camera_mode_text.text != f'Camera Mode: {mode}':
            if 'Noise' in self.camera_mode_text.text:
                camera_noise_seq.pause()
            self.camera_mode_text.text = f'Camera Mode: {mode}'
            match mode:
                case 'Blur Noise':
                    camera.clip_plane_far = 1400
                    camera.shader_setter(camera_blur_noise_shader)
                    camera_noise_seq.start()
                case 'None':
                    camera.shader_setter(None)

pause_menu = PauseMenu()

# lighting

def enable_lighting():

    global torch#, torch_light_1, torch_light_2
    scene.fog_density = 0.2
    scene.fog_color = color.black
    torch = Entity(model="flashlight.gltf", scale=0.3)
    torch_light_1 = SpotLight(parent=torch, color=color.white, position=(3, 0.5, 4.2), rotation=(0, -135, -5)) # noqa: F841
    torch_light_2 = SpotLight(parent=torch, color=color.white, position=(3, 0.5, 4.2), rotation=(0, -135, -5)) # noqa: F841
    # torch_light_3 = SpotLight(parent=torch, color=color.white, position=(3, 0.5, 4.2), rotation=(0, -135, -5)) # noqa: F841
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
        vert_2_y = randchoice([avg, avg+.1, avg+.2, avg-.1, avg-.2])
        new_vertices[0][1] = vert_0_y
        new_vertices[1][1] = vert_1_y
        new_vertices[2][1] = vert_2_y
        new_vertices[3][1] = vert_3_y

    elif terrain_beside:
        vert_0_y = terrain[(x-1, z)]['vertices'][1][1]
        vert_3_y = terrain[(x-1, z)]['vertices'][2][1]
        avg = (vert_0_y + vert_3_y)/2
        vert_1_y = randchoice([avg, avg+.1, avg+.2, avg-.1, avg-.2])
        avg = (vert_0_y + vert_1_y + vert_3_y)/3
        vert_2_y = randchoice([avg, avg+.1, avg+.2, avg-.1, avg-.2])
        new_vertices[0][1] = vert_0_y
        new_vertices[1][1] = vert_1_y
        new_vertices[2][1] = vert_2_y
        new_vertices[3][1] = vert_3_y

    elif terrain_below:
        vert_0_y = terrain[(x, z-1)]['vertices'][3][1]
        vert_1_y = terrain[(x, z-1)]['vertices'][2][1]
        avg = (vert_0_y + vert_1_y)/2
        vert_2_y = randchoice([avg, avg+.1, avg+.2, avg-.1, avg-.2])
        avg = (vert_0_y + vert_1_y + vert_2_y)/3
        vert_3_y = randchoice([avg, avg+.1, avg+.2, avg-.1, avg-.2])
        new_vertices[0][1] = vert_0_y
        new_vertices[1][1] = vert_1_y
        new_vertices[2][1] = vert_2_y
        new_vertices[3][1] = vert_3_y

    else:
        new_vertices[0][1] = randchoice([0, .1, .2, -.1, -.2])
        new_vertices[1][1] = randchoice([0, .1, .2, -.1, -.2])
        new_vertices[2][1] = randchoice([0, .1, .2, -.1, -.2])
        new_vertices[3][1] = randchoice([0, .1, .2, -.1, -.2])

    global lowest_y, highest_y
    lowest_y = min(lowest_y, new_vertices[0][1], new_vertices[1][1], new_vertices[2][1], new_vertices[3][1]) # pylint: disable=used-before-assignment
    highest_y = max(highest_y, new_vertices[0][1], new_vertices[1][1], new_vertices[2][1], new_vertices[3][1]) # pylint: disable=used-before-assignment

    return new_vertices

lowest_y = 0
highest_y = 0
terrain = {}

for x in range(-settings['world_size'], settings['world_size']+1):
    for z in range(-settings['world_size'], settings['world_size']+1):
        terrain[(x, z)] = {}
        terrain[(x, z)]['entity'] = None
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

    mesh = Mesh(vertices=vertices, triangles=triangles, uvs=uvs)
    mesh.generate_normals()
    terrain[pos]['entity'] = Entity(model=mesh, collider="mesh", texture=randchoice(textures, p=weights), ignore=True)
    terrain[pos]['entity'].collision = False

    if randchoice([0, 1], p=[0.95, 0.05]) or settings['world_size'] in pos or -settings['world_size'] in pos:

        y_rot = randint(0, 90)
        x_rot = randint(-5, +5)
        z_rot = randint(-5, +5)
        tree_height = randchoice(settings['tree_heights'])
        leaves_level_start = tree_height-3
        leaves_level_current = 1
        next_pos = Vec3(pos[0], min(vertices[0][1], vertices[1][1], vertices[2][1], vertices[3][1]), pos[1])

        # Create a parent entity for the tree
        tree = Entity(ignore=True, parent=terrain[pos]['entity'])

        for _ in range(tree_height):
            log = Entity(model="cube", collider="box", texture=tree_log_texture, position=next_pos, rotation=(x_rot, y_rot, z_rot), ignore=True, parent=tree)
            log.collision = False
            if _ > leaves_level_start:
                match leaves_level_current:
                    case 1:
                        back_2 = log.back + log.back
                        forward_2 = log.forward + log.forward
                        left_2 = log.left + log.left
                        right_2 = log.right + log.right
                        for _pos in [log.back + left_2, left_2, log.forward + left_2, back_2 + log.left, forward_2 + log.left, back_2, forward_2, back_2 + log.right, forward_2 + log.right, log.back + right_2, right_2, log.forward + right_2]:
                            leaf = Entity(model="cube", texture=tree_leaves_texture, position=next_pos + _pos, rotation=(x_rot, y_rot, z_rot), ignore=True, parent=tree)
                            leaf.collision = False
                    case 2:
                        for _pos in [log.back + log.left, log.left, log.forward + log.left, log.back, log.forward, log.back + log.right, log.right, log.forward + log.right]:
                            leaf = Entity(model="cube", texture=tree_leaves_texture, position=next_pos + _pos, rotation=(x_rot, y_rot, z_rot), ignore=True, parent=tree)
                            leaf.collision = False
                leaves_level_current += 1
            y_rot = randint(y_rot - 5, y_rot + 5)
            x_rot = randint(x_rot - 5, x_rot + 5)
            z_rot = randint(z_rot - 5, z_rot + 5)
            next_pos += log.up

    elif randchoice([0, 1], p=[0.90, 0.1]):

        _vertices = vertices.copy()
        _vertices[0][1] += 0.01
        _vertices[1][1] += 0.01
        _vertices[2][1] += 0.01
        _vertices[3][1] += 0.01

        mesh = Mesh(vertices=_vertices, triangles=triangles, uvs=uvs)
        mesh.generate_normals()
        entity = Entity(model=mesh, collider="mesh", texture=randchoice(leaves_textures), ignore=True, parent=terrain[pos]['entity'])
        entity.collision = False

# load / unload entities

def first_load():

    for x in range(int(player.x) - settings['render_dist'], int(player.x) + settings['render_dist'] + 1):
        for z in range(int(player.z) - settings['render_dist'], int(player.z) + settings['render_dist'] + 1):
            pos = (x, z)
            if pos not in rendered_chunks and pos in terrain:
                if not terrain[pos]['entity']:
                    create_entity(pos, terrain[pos]['vertices'])
                else:
                    terrain[pos]['entity'].enabled = True
                rendered_chunks[pos] = None
            render_grid[pos] = None

    for x in range(int(player.x) - settings['collision_dist'], int(player.x) + settings['collision_dist'] + 1):
        for z in range(int(player.z) - settings['collision_dist'], int(player.z) + settings['collision_dist'] + 1):
            pos = (x, z)
            if pos in rendered_chunks:
                terrain[pos]['entity'].collision = True
                for _ in terrain[pos]['entity'].children_getter():
                    _.collision = True
                    for __ in _.children_getter()[:4]:
                        __.collision = True
            collision_grid[pos] = None

def reset_render_grid():

    global render_grid

    _render_grid = {}
    for x in range(int(player.x) - settings['render_dist'], int(player.x) + settings['render_dist'] + 1):
        for z in range(int(player.z) - settings['render_dist'], int(player.z) + settings['render_dist'] + 1):
            pos = (x, z)
            render_grid[pos] = None
            _render_grid[pos] = None
            if pos not in r_loop and pos not in rendered_chunks and pos in terrain:
                r_loop.append(pos)
    render_grid = _render_grid.copy()

def reset_collision_grid():

    global collision_grid

    _collision_grid = {}
    for x in range(int(player.x) - settings['collision_dist'], int(player.x) + settings['collision_dist'] + 1):
        for z in range(int(player.z) - settings['collision_dist'], int(player.z) + settings['collision_dist'] + 1):
            pos = (x, z)
            _collision_grid[pos] = None
            if pos not in collision_grid and pos in rendered_chunks:
                collision_grid[pos] = None
                c_loop.append(pos)
    collision_grid = _collision_grid.copy()

def render_loop():

    try:
        pos = r_loop.pop(0)
        if not terrain[pos]['entity']:
            create_entity(pos, terrain[pos]['vertices'])
        else:
            terrain[pos]['entity'].enabled = True
        rendered_chunks[pos] = None
    except IndexError:
        pass

def collision_loop():

    try:
        pos = c_loop.pop(0)
        terrain[pos]['entity'].collision = True
        for _ in terrain[pos]['entity'].children_getter():
            _.collision = True
            for __ in _.children_getter()[:4]:
                __.collision = True
    except IndexError:
        pass

def unload():

    to_unload = []

    for pos in rendered_chunks:
        if pos not in render_grid:
            _ = destroy(terrain[pos]['entity'])
            terrain[pos]['entity'] = None
            to_unload.append(pos)
        elif pos not in collision_grid:
            terrain[pos]['entity'].collision = False
            for _ in terrain[pos]['entity'].children_getter():
                _.collision = False
                for __ in _.children_getter()[:4]:
                    __.collision = False

    for pos in to_unload:
        del rendered_chunks[pos]

# other stuff

def check_player_y():
    if player.y < lowest_y:
        player.position = (0, highest_y, 0)

seq_vars = {
    'duration': 0,
    'magnitude': 0,
}

def max_stress_event():

    magnitude = random.uniform(0.5, 2)
    duration = random.uniform(1, 3)/4
    seq_vars['duration'] = duration
    seq_vars['magnitude'] = magnitude

def update_shader_values():
    camera.set_shader_input("noise_offset", random.randint(0, 100)/100)

    while True:
        try:
            stress = player_stress['levels'][::player_stress['direction']][player_stress['index']]
            break
        except IndexError:
            if player_stress['direction'] == 1:
                Sequence(
                    Func(max_stress_event),
                    Func(camera.shake, duration = seq_vars['duration'], magnitude = seq_vars['magnitude']),
                    Wait(seq_vars['duration']),
                    Func(camera.shake, duration = seq_vars['duration'], magnitude = seq_vars['magnitude']/3),
                    Wait(seq_vars['duration']),
                    Func(camera.shake, duration = seq_vars['duration'], magnitude = seq_vars['magnitude']/3),
                    Wait(seq_vars['duration']),
                    Func(camera.shake, duration = seq_vars['duration'], magnitude = seq_vars['magnitude']/4),
                ).start()
            player_stress['direction'] *= -1
            player_stress['index'] = 0
    player_stress['index'] += 1

    camera.set_shader_input("blur_size", stress)
    camera.set_shader_input("noise_strength", stress+0.075)

def input(key): # pylint: disable=function-redefined

    match key:
        case 'escape':
            if pause_menu.pause_menu.enabled:
                pause_menu.resume_game()
            else:
                pause_menu.pause_game()
        # case 'f':
        #     print('f pressed!')
        #     if torch.enabled_getter():
        #         torch.disable()
        #         # torch_light_2.disable()
        #     else:
        #         torch.enable()
        #         # torch_light_2.enable()


r_loop = []
render_grid = {}
rendered_chunks = {}

c_loop = []
collision_grid = {}

player.position = (0, 100, 0)
first_load()

sequence_1 = Sequence(Func(check_player_y), Wait(5), loop=True)
sequence_2 = Sequence(Func(reset_render_grid), Wait(0.25), loop=True)
sequence_3 = Sequence(Func(render_loop), Wait(0.005), loop=True)
sequence_4 = Sequence(Func(reset_collision_grid), Wait(0.25), loop=True)
sequence_5 = Sequence(Func(collision_loop), Wait(0.05), loop=True)
sequence_6 = Sequence(Func(unload), Wait(1), loop=True)
camera_noise_seq = Sequence(Func(update_shader_values), loop=True)

pause_menu.change_camera_mode('Blur Noise')
pause_menu.pause_game()

sequence_1.start()
sequence_2.start()
sequence_3.start()
sequence_4.start()
sequence_5.start()
sequence_6.start()

ambiance_trees = Audio("ambiance_trees.m4a", loop=True, autoplay=True, volume=1)
ambiance_crickets = Audio("ambiance_crickets.m4a", loop=True, autoplay=True, volume=1)

app.run()
