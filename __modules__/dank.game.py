import os
import numpy as np
import pretty_errors
from dankware import clr, cls
from numpy.random import choice as randchoice
from numpy.random import randint, uniform
from perlin_noise import PerlinNoise
from PIL import Image
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.prefabs.health_bar import HealthBar
from ursina.prefabs.splash_screen import SplashScreen
from ursina.scripts.smooth_follow import SmoothFollow
from direct.filter.CommonFilters import CommonFilters

cls()

os.chdir(os.path.dirname(__file__))

if '__compiled__' in globals() and 'DANK_TOOL_VERSION' not in os.environ:
    # rediect stderr to a file
    if os.path.isfile('dank.game.log'):
        os.remove('dank.game.log')
    file = open('dank.game.log', 'w', encoding='utf-8')
    sys.stderr = file

input(clr("""\n  [ DISCLAIMER ]

  - This game is in early development, expect bugs!
  - If the ground is not visible, restart the game!
  - You might need to use max brightness!
  - Game updates might be slow!
  - Built with Ursina Engine!

  [ CONTROLS ]

  - WASD to move
  - SHIFT to sprint
  - SPACE to jump
  - ESC to pause / quit game

  > Press [ENTER] to start...
"""))

# game settings

settings = {
    'development_mode': False,
    'enable_lighting': True,
    'enable_pixelation': True,
    'player_speed': 2.5,
    'player_sprint_speed': 5,
    'player_jump_height': 1,
    'stamina_max': 40,  # Maximum stamina
    'stamina_regen_rate': 5,  # Stamina regeneration per second
    'stamina_drain_rate': 25,  # Stamina drain per second when sprinting
    'stamina_jump_cost': 10,
    'world_size': 40, # n*2 x n*2 # default: 250
    'chunk_size': 16,  # Size of each terrain chunk
    'render_dist': 2, # n*chunk_size x n*chunk_size
    'player_y_min': -10,
    'player_y_max': 100,
    'perlin_scale': 50.0,  # Scale factor for Perlin noise (larger = smoother terrain)
    'perlin_octaves': 6,  # Number of octaves for Perlin noise (more octaves = more detail)
    'amplitude': 3.0,  # Height amplitude for terrain (lower = gentler slopes)
    'entity_gen_delay': 0.1,
    'tree_heights': list(range(7, 14)),
    'camera_tilt_amount': 5.0,  # Maximum tilt angle in degrees
    'camera_tilt_speed': 3.0,   # How quickly the camera tilts
    'camera_return_speed': 2.0, # How quickly the camera returns to neutral
}

# Function to generate terrain textures
def generate_terrain_textures():

    if '__compiled__' in globals():
        os.chdir('ursina')

    textures = {
        load_texture("grass1"): 0.445,
        load_texture("grass2"): 0.445,
        load_texture("mossy_cobblestone1"): 0.05,
        load_texture("mossy_cobblestone2"): 0.05,
        load_texture("mossy_stone_bricks"): 0.01,
    }

    # Get the original textures and weights
    weights = list(textures.values())
    textures = list(textures.keys())

    # Ensure textures directory exists
    os.makedirs("textures/tmp", exist_ok=True)

    # Generate 10 terrain textures
    for i in range(1, 11):
        # Create a 256x256 output image (16x16 grid of textures, each cell is 16x16 pixels)
        terrain_img = Image.new("RGBA", (256, 256))

        # For each cell in the 16x16 grid
        for grid_x in range(16):
            for grid_y in range(16):
                # Choose a texture based on weights
                texture_idx = np.random.choice(len(textures), p=weights)
                texture = textures[texture_idx]

                # Calculate the position in the output image (each cell is 16x16 pixels)
                start_x = grid_x * 16
                start_y = grid_y * 16

                # Copy the exact texture data for this 16x16 cell
                for local_x in range(16):
                    for local_y in range(16):
                        # Get the exact pixel from the texture
                        # We use modulo to ensure we stay within the texture's dimensions
                        # (in case the texture is smaller than 16x16)
                        # Apply random rotation by shifting coordinates
                        rotation = np.random.randint(0, 4)  # 0, 90, 180, or 270 degrees
                        if rotation == 0:  # 0 degrees
                            texture_x = local_x % texture.width
                            texture_y = local_y % texture.height
                        elif rotation == 1:  # 90 degrees
                            texture_x = local_y % texture.width
                            texture_y = (texture.width - local_x - 1) % texture.height
                        elif rotation == 2:  # 180 degrees
                            texture_x = (texture.width - local_x - 1) % texture.width
                            texture_y = (texture.height - local_y - 1) % texture.height
                        else:  # 270 degrees
                            texture_x = (texture.width - local_y - 1) % texture.width
                            texture_y = local_x % texture.height

                        # Get the exact color from the texture at this position
                        color_data = texture.get_pixel(texture_x, texture_y)

                        # Set the corresponding pixel in our terrain image
                        terrain_img.putpixel((start_x + local_x, start_y + local_y), (
                            int(color_data[0] * 255),
                            int(color_data[1] * 255),
                            int(color_data[2] * 255),
                            255
                        ))

        # Save the image
        terrain_img.save(f"textures/tmp/terrain_{i}.png")

# Function to generate tree models
def generate_tree_models():

    # Ensure directory exists
    os.makedirs("models_compressed/tmp", exist_ok=True)

    # Generate 10 sets of tree models
    for i in range(1, 11):
        # Create parent entities for logs and leaves
        tree_logs = Entity(ignore=True)
        tree_leaves = Entity(ignore=True)

        # Random rotation for the tree
        y_rot = 0
        x_rot = randint(-5, +5)
        z_rot = randint(-5, +5)

        # Random tree height
        tree_height = randchoice(settings['tree_heights'])
        leaves_level_start = tree_height-3
        leaves_level_current = 1

        # Position at origin (will be repositioned when placed)
        next_pos = Vec3(0, 0, 0)

        # Generate the tree structure
        for level in range(tree_height):
            log = Entity(model="cube",
                        position=next_pos, rotation=(x_rot, y_rot, z_rot),
                        ignore=True, parent=tree_logs)

            if level > leaves_level_start:
                match leaves_level_current:
                    case 1:
                        back_2 = log.back + log.back
                        forward_2 = log.forward + log.forward
                        left_2 = log.left + log.left
                        right_2 = log.right + log.right
                        for leaf_pos in [log.back + left_2, left_2, log.forward + left_2,
                                        back_2 + log.left, forward_2 + log.left, back_2, forward_2,
                                        back_2 + log.right, forward_2 + log.right,
                                        log.back + right_2, right_2, log.forward + right_2]:
                            leaf = Entity(model="cube",
                                        position=next_pos + leaf_pos, rotation=(x_rot, y_rot, z_rot),
                                        ignore=True, parent=tree_leaves)
                    case 2:
                        for leaf_pos in [log.back + log.left, log.left, log.forward + log.left,
                                        log.back, log.forward, log.back + log.right,
                                        log.right, log.forward + log.right]:
                            leaf = Entity(model="cube",
                                        position=next_pos + leaf_pos, rotation=(x_rot, y_rot, z_rot),
                                        ignore=True, parent=tree_leaves)
                leaves_level_current += 1

            y_rot = randint(y_rot - 5, y_rot + 5)
            x_rot = randint(x_rot - 5, x_rot + 5)
            z_rot = randint(z_rot - 5, z_rot + 5)
            next_pos += log.up

        # Combine meshes for efficiency
        tree_logs.combine(include_normals=True)
        tree_leaves.combine(include_normals=True)

        # Save the models
        tree_logs.model.save(f"tree_log_{i}", Path("models_compressed/tmp"))
        tree_leaves.model.save(f"tree_leaves_{i}", Path("models_compressed/tmp"))

        # Destroy the temporary entities
        destroy(tree_logs)
        destroy(tree_leaves)

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

blur_noise_pixel_shader = Shader(
    name='blur_noise_pixel_shader',
    fragment='''
    #version 430

    uniform sampler2D tex;
    in vec2 uv;
    // pixelation parameter: if <= 0, skip pixelation
    uniform float PixelCount;
    // blur & noise parameters
    uniform float blur_size;
    uniform float noise_offset;
    uniform float noise_strength;

    out vec4 color;

    // 1) vertical blur
    vec4 apply_vertical_blur(vec2 uv) {
        vec4 col = vec4(0.0);
        for (float i = 0.0; i < 10.0; i++) {
            float f = (i / 9.0 - 0.5);
            vec2 off = vec2(0.0, f * blur_size);
            col += texture(tex, uv + off);
        }
        return col * 0.1;
    }

    // 2) simple hash‑based noise
    vec3 apply_noise(vec3 rgb, vec2 uv) {
        float n = fract(sin(dot(uv + noise_offset, vec2(12.9898, 78.233))) * 43758.5453);
        n = (n - 0.5) * noise_strength;
        return rgb + n;
    }

    void main() {
        vec2 use_uv = uv;

        // 3) conditional pixelation
        if (PixelCount > 0.0) {
            float dx = 9.0  * (1.0 / PixelCount);
            float dy = 16.0 * (1.0 / PixelCount);
            use_uv = vec2(
                dx * floor(uv.x / dx),
                dy * floor(uv.y / dy)
            );
        }

        // apply blur + noise to either quantized or original uv
        vec4 blurred = apply_vertical_blur(use_uv);
        vec3 noised  = apply_noise(blurred.rgb, uv);

        color = vec4(noised, 1.0);
    }
    ''',
    default_input={
        'blur_size':      0.0,    # up to ~0.1
        'noise_offset':   1.0,    # animate for rolling grain
        'noise_strength': 0.0,    # up to ~0.1
        'PixelCount':     3200.0 if settings['enable_pixelation'] else 0.0,
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
            # self.camera_mode_text.disable()
            for button in (self.render_mode_buttons): # + self.camera_mode_buttons
                button.disable()

        self.resume_button = Button(text='Resume', parent=self.pause_menu, scale=(0.15, 0.05), position=(0, 0.0375), color=color.green, radius=0.25)
        self.quit_button = Button(text='Quit', parent=self.pause_menu, scale=(0.15, 0.05), position=(0, -0.0375), color=color.red, radius=0.25)
        self.resume_button.on_click = self.resume_game
        self.quit_button.on_click = self.quit_game

    def pause_game(self):
        # ambiance_trees.pause()
        # ambiance_crickets.pause()
        self.pause_menu.enabled = True
        application.paused = True
        mouse.visible = True
        player.disable()
        time.dt = 0

    def resume_game(self):
        # ambiance_trees.resume()
        # ambiance_crickets.resume()
        self.pause_menu.enabled = False
        application.paused = False
        mouse.visible = False
        player.enable()
        time.dt = 1

    def quit_game(self):
        if '__compiled__' in globals():
            if "DANK_TOOL_VERSION" in os.environ:
                os.system("taskkill /f /im dank.tool.exe")
            else:
                os.system("taskkill /f /im dank.game.exe")
        else:
            application.quit()

    def change_render_mode(self, mode):
        if window.render_mode != mode:
            self.render_mode_text.text = f'Render Mode: {mode}'
            window.render_mode = mode

    def change_camera_mode(self, mode):
        if self.camera_mode_text.text != f'Camera Mode: {mode}':
            if 'Noise' in self.camera_mode_text.text and not player_stress_sequence.paused:
                player_stress_sequence.pause()
            self.camera_mode_text.text = f'Camera Mode: {mode}'
            match mode:
                case 'Blur Noise':
                    camera.clip_plane_far = 1400
                    if settings['enable_pixelation'] and camera.shader_input_getter().get('PixelCount', 0.0) == 0.0:
                        camera.set_shader_input("PixelCount", 3200.0)
                    camera.shader_setter(blur_noise_pixel_shader)
                    if not player_stress_sequence.started:
                        player_stress_sequence.start()
                    elif player_stress_sequence.paused:
                        player_stress_sequence.resume()
                case 'None':
                    if settings['enable_pixelation'] and camera.shader_input_getter().get('PixelCount', 3200.0) != 0.0:
                        camera.set_shader_input("PixelCount", 0.0)
                    camera.shader_setter(None)

# lighting

def enable_lighting():

    global torch_light

    scene.fog_density = 0.2
    scene.fog_color = color.black
    torch = Entity(model="flashlight.gltf", scale=0.3)

    torch_light = SpotLight(
        parent=torch,
        color=color.white * 10,
        position=(3, 0.5, 4.2),
        rotation=(0, -135, -5),
    )

    torch_light_glow = PointLight(
        parent=torch,
        color=color.white * 0.25,
        position=(3, 0.5, 4.2),
    )

    torch_light._light.setExponent(90)
    torch_light._light.setAttenuation(Vec3(1, 0.2, 0.05))
    torch_light_glow._light.setAttenuation(Vec3(1, 0.5, 0.1))

    player_camera = Entity(parent=camera, position=(0.5, -0.5, 0.8), rotation=(0, 135, 5))
    torch.add_script(SmoothFollow(target=player_camera, rotation_speed=10))

def enable_filters():

    # Setup CommonFilters for advanced visual effects
    filters = CommonFilters(app.win, app.cam)

    # Enable ambient occlusion for better depth perception
    filters.setAmbientOcclusion(
        numsamples=16,
        radius=0.05,
        amount=2.0,
        strength=0.01,
        falloff=0.000002
    )

    # Enable HDR for better light handling
    filters.setHighDynamicRange()

    # Add exposure adjustment for the HDR
    filters.setExposureAdjust(stops=0.5)

    # Enable MSAA for smoother edges
    # filters.setMSAA(samples=4)

# Function to get height at a specific position
def get_height(x, z):
    # Scale the coordinates to get smoother terrain
    nx = x / settings['perlin_scale']
    nz = z / settings['perlin_scale']

    # Use multiple noise layers for more interesting terrain
    base_height = perlin([nx, nz]) * settings['amplitude']

    # Add some smaller details with higher frequency
    detail = perlin([nx * 2, nz * 2]) * (settings['amplitude'] * 0.3)

    # Add some very small details for texture
    micro_detail = perlin([nx * 4, nz * 4]) * (settings['amplitude'] * 0.1)

    # Combine all layers
    return base_height + detail + micro_detail

# Function to generate chunk mesh
def generate_chunk_mesh(chunk_x, chunk_z):
    chunk_size = settings['chunk_size']
    vertices = []
    triangles = []
    uvs = []
    normals = []

    # Generate vertices grid for the chunk
    for z in range(chunk_size + 1):
        for x in range(chunk_size + 1):
            world_x = chunk_x * chunk_size + x
            world_z = chunk_z * chunk_size + z
            height = get_height(world_x, world_z)
            vertices.append(Vec3(world_x, height, world_z))
            uvs.append((x/chunk_size, z/chunk_size))
            # Add an upward-facing normal for each vertex
            normals.append(Vec3(0, 1, 0))

    # Generate triangles (2 per grid cell)
    for z in range(chunk_size):
        for x in range(chunk_size):
            # Get indices of the 4 corners of the current grid cell
            i = z * (chunk_size + 1) + x
            i_right = i + 1
            i_below = i + (chunk_size + 1)
            i_below_right = i_below + 1

            # Add two triangles to form a quad (flipped order for correct facing)
            triangles.extend([i, i_right, i_below])
            triangles.extend([i_right, i_below_right, i_below])

    # Create mesh with explicit normals
    mesh = Mesh(vertices=vertices, triangles=triangles, uvs=uvs, normals=normals)
    return mesh

# terrain and entity generation

def create_chunk_entity(chunk_pos):

    # Create entity for the chunk
    chunk_entity = Entity(
        model=generate_chunk_mesh(chunk_pos[0], chunk_pos[1]),
        collider="mesh",
        texture=randchoice(textures),
        position=(0, 0, 0),
        ignore=True,
        alpha=0,
    )

    # Add trees and vegetation to the chunk
    add_vegetation_to_chunk(chunk_pos, chunk_entity)

    for child in chunk_entity.get_descendants():
        child.fade_in(duration=1)
    chunk_entity.fade_in(duration=1)

    chunks[chunk_pos] = chunk_entity

def add_vegetation_to_chunk(chunk_pos, chunk_entity):
    chunk_size = settings['chunk_size']

    # Add some trees randomly within the chunk
    for _ in range(int(chunk_size * chunk_size * 0.01)):  # 1% density
        # Random position within the chunk
        local_x = randint(0, chunk_size-1)
        local_z = randint(0, chunk_size-1)
        world_x = chunk_pos[0] * chunk_size + local_x
        world_z = chunk_pos[1] * chunk_size + local_z

        # Get height at this position
        height = get_height(world_x, world_z)

        # Randomly select one of the 10 tree models
        tree_model_num = randint(1, 10)
        rotation = (0, randint(0, 360), 0) # Random Y rotation

        # Load the corresponding tree log and leaves models
        _ = Entity(
            model=f"models_compressed/tmp/tree_log_{tree_model_num}",
            texture=tree_log_texture,
            collider = "mesh",
            position=(world_x, height, world_z),
            rotation=rotation,
            ignore=True,
            parent=chunk_entity,
            alpha=0,
        )

        _ = Entity(
            model=f"models_compressed/tmp/tree_leaves_{tree_model_num}",
            texture=tree_leaves_texture,
            position=(world_x, height, world_z),
            rotation=rotation,
            ignore=True,
            parent=chunk_entity,
            alpha=0,
        )

    # Add some ground vegetation (grass, flowers, etc.)
    for _ in range(int(chunk_size * chunk_size * 0.05)):  # 5% density
        local_x = randint(0, chunk_size-1)
        local_z = randint(0, chunk_size-1)
        world_x = chunk_pos[0] * chunk_size + local_x
        world_z = chunk_pos[1] * chunk_size + local_z

        # Get height at this position
        height = get_height(world_x, world_z)

        # Create vegetation entity
        _ = Entity(
            model="cube",
            position=(world_x, height, world_z),
            rotation=(randint(-5, 5), randint(0, 90), randint(-5, 5)),
            texture=randchoice(ground_leaves_textures),
            ignore=True,
            parent=chunk_entity,
            alpha=0,
        )

# load / unload chunks

def first_load():
    # Calculate player's chunk position
    player_chunk_x = int(player.x) // settings['chunk_size']
    player_chunk_z = int(player.z) // settings['chunk_size']

    for cx in range(player_chunk_x - settings['render_dist'], player_chunk_x + settings['render_dist'] + 1):
        for cz in range(player_chunk_z - settings['render_dist'], player_chunk_z + settings['render_dist'] + 1):
            chunk_pos = (cx, cz)
            if chunk_pos not in rendered_chunks:
                create_chunk_entity(chunk_pos)
                rendered_chunks[chunk_pos] = None
            render_grid[chunk_pos] = None

    game_sequence_1.start()
    game_sequence_2.start()

def render_chunks():
    global render_grid

    # Calculate player's chunk position
    player_chunk_x = int(player.x) // settings['chunk_size']
    player_chunk_z = int(player.z) // settings['chunk_size']

    # Update render grid based on player's position
    _render_grid = {}
    r_loop = []

    for cx in range(player_chunk_x - settings['render_dist'], player_chunk_x + settings['render_dist'] + 1):
        for cz in range(player_chunk_z - settings['render_dist'], player_chunk_z + settings['render_dist'] + 1):
            chunk_pos = (cx, cz)
            _render_grid[chunk_pos] = None

            # Add chunk to render loop if not already rendered or in queue
            if chunk_pos not in r_loop and chunk_pos not in rendered_chunks:
                r_loop.append(chunk_pos)

    render_grid = _render_grid

    # Render loop functionality
    for chunk_pos in r_loop:
        create_chunk_entity(chunk_pos)
        rendered_chunks[chunk_pos] = None

def unload_chunks():
    to_unload = []

    # Unload chunks that are no longer in render distance
    for chunk_pos in list(rendered_chunks.keys()):
        if chunk_pos not in render_grid:
            # Unload chunk completely
            if chunk_pos in chunks:
                for child in chunks[chunk_pos].get_descendants():
                    child.fade_out(duration=1)
                chunks[chunk_pos].fade_out(duration=1)
                Sequence(
                    Wait(1),
                    Func(destroy, chunks[chunk_pos]),
                    auto_destroy=True,
                ).start()
                del chunks[chunk_pos]
            to_unload.append(chunk_pos)

    # Remove unloaded chunks from tracking
    for chunk_pos in to_unload:
        if chunk_pos in rendered_chunks:
            del rendered_chunks[chunk_pos]

def update_stamina():
    if player.is_sprinting:
        player.stamina = max(0, player.stamina - settings['stamina_drain_rate'] * time.dt)
        stamina_bar.value_setter(player.stamina)
        if player.stamina <= 0:
            player.is_sprinting = False
            player.speed = settings['player_speed']
    else:
        player.stamina = min(settings['stamina_max'], player.stamina + settings['stamina_regen_rate'] * time.dt)
        stamina_bar.value_setter(player.stamina)
        if player.stamina >= settings['stamina_max'] and stamina_bar.bar.color == color.white:
            _ = Sequence(
                Func(stamina_bar.bar.blink, duration=1),
                Wait(1),
                Func(stamina_bar.bar.blink, duration=1),
                Wait(1),
                Func(stamina_bar.bar.animate_color, color.clear, duration=1),
                auto_destroy=True,
            ).start()

seq_vars = {
    'duration': 0,
    'magnitude': 0,
}

def update_shader_values():
    camera.set_shader_input("noise_offset", randint(0, 100)/100)

    while True:
        try:
            stress = player_stress['levels'][::player_stress['direction']][player_stress['index']]
            break
        except IndexError:
            if player_stress['direction'] == 1:
                seq_vars['magnitude'] = uniform(0.5, 2)
                seq_vars['duration'] = uniform(1, 3)/4
                Sequence(
                    Func(camera.shake, duration = seq_vars['duration'], magnitude = seq_vars['magnitude']),
                    Wait(seq_vars['duration']),
                    Func(camera.shake, duration = seq_vars['duration'], magnitude = seq_vars['magnitude']/3),
                    Wait(seq_vars['duration']),
                    Func(camera.shake, duration = seq_vars['duration'], magnitude = seq_vars['magnitude']/3),
                    Wait(seq_vars['duration']),
                    Func(camera.shake, duration = seq_vars['duration'], magnitude = seq_vars['magnitude']/4),
                    auto_destroy=True,
                ).start()
            player_stress['direction'] *= -1
            player_stress['index'] = 0
    player_stress['index'] += 1

    camera.set_shader_input("blur_size", stress)
    camera.set_shader_input("noise_strength", stress+0.075)
    camera.fov = 90 - stress*200

def update_camera_tilt():

    # Smoothly interpolate current rotation to target rotation
    # current_x_tilt = player.camera_pivot.rotation_x

    # if not held_keys['w'] and not held_keys['s']:
    #     seq_vars['cam_x'] = current_x_tilt

    # target_x_tilt = current_x_tilt
    target_y_tilt = 0
    target_z_tilt = 0

    # Set target tilts based on movement keys
    # if held_keys['w']: target_x_tilt = settings['camera_tilt_amount'] + seq_vars['cam_x']
    # if held_keys['s']: target_x_tilt = -settings['camera_tilt_amount'] + seq_vars['cam_x']
    if held_keys['a']:
        target_y_tilt = -settings['camera_tilt_amount']
        target_z_tilt = -settings['camera_tilt_amount']
    if held_keys['d']:
        target_y_tilt = settings['camera_tilt_amount']
        target_z_tilt = settings['camera_tilt_amount']

    # Use different speeds for tilting and returning to neutral
    # x_speed = settings['camera_tilt_speed'] if abs(target_x_tilt) > 0 else settings['camera_return_speed']
    y_speed = settings['camera_tilt_speed'] if abs(target_y_tilt) > 0 else settings['camera_return_speed']
    z_speed = settings['camera_tilt_speed'] if abs(target_z_tilt) > 0 else settings['camera_return_speed']

    # Apply smooth interpolation
    # player.camera_pivot.rotation_x = lerp(current_x_tilt, target_x_tilt, time.dt * x_speed)
    player.camera_pivot.rotation_y = lerp(player.camera_pivot.rotation_y, target_y_tilt, time.dt * y_speed)
    player.camera_pivot.rotation_z = lerp(player.camera_pivot.rotation_z, target_z_tilt, time.dt * z_speed)

def check_player_y():
    if player.y < settings['player_y_min']:
        player.position = (0, settings['player_y_max'], 0)
        if settings['development_mode']:
            print(clr(f"  - updated player y: {player.y}"))

def input(key): # pylint: disable=function-redefined

    match key:
        case 'escape':
            if pause_menu.pause_menu.enabled:
                pause_menu.resume_game()
            else:
                pause_menu.pause_game()
        case 'shift':
            if player.stamina > 0:
                player.is_sprinting = True
                player.speed = settings['player_sprint_speed']
                if stamina_bar.bar.color == color.clear:
                    stamina_bar.bar.animate_color(color.white, duration=0.3)
        case 'shift up':
            player.is_sprinting = False
            player.speed = settings['player_speed']
        case 'space':
            if not isinstance(player, EditorCamera) and player.stamina > settings['stamina_jump_cost']:
                player.jump()
                player.stamina -= settings['stamina_jump_cost']
                stamina_bar.value_setter(player.stamina)
                if stamina_bar.bar.color == color.clear:
                    stamina_bar.bar.animate_color(color.white, duration=0.3)

app = Ursina(
    title='𝚍𝚊𝚗𝚔.𝚐𝚊𝚖𝚎',
    icon = (os.path.join(os.path.dirname(__file__), "dankware.ico") if '__compiled__' in globals() else 'textures/ursina.ico'),
    borderless=not settings['development_mode'],
    fullscreen=not settings['development_mode'],
    development_mode=settings['development_mode'],
)

Entity.default_shader = None
application.ursina_splash = SplashScreen('dankware.png')

# Generate the terrain textures
print(clr("  - Generating terrain textures..."))
generate_terrain_textures()

# Generate tree models
print(clr("  - Generating tree models..."))
tree_log_texture = load_texture("acacia_log")
tree_leaves_texture = load_texture("azalea_leaves")
generate_tree_models()

# Use the generated textures
textures = tuple(load_texture(f"tmp/terrain_{i}") for i in range(1, 11))
ground_leaves_textures = tuple([
    load_texture("mangrove_leaves_inventory"),
    load_texture("azalea_leaves"),
    load_texture("flowering_azalea_leaves")
])

# Create stamina bar
stamina_bar = HealthBar(
    name = 'stamina_bar',
    max_value = settings['stamina_max'],
    value = settings['stamina_max'],
    color = color.clear,
    bar_color = color.clear,
    highlight_color = color.clear,
    roundness = 0.15,
    scale = (.3, .01),
    position = (0, -.50),
    origin = (0, 0),
    parent = camera.ui,
    show_text = False,
)

# Initialize Perlin noise generator
perlin = PerlinNoise(octaves=settings['perlin_octaves'], seed=int(time.time()))
chunks = {}
render_grid = {}
rendered_chunks = {}

# player = EditorCamera(move_speed=15, zoom_speed=1)
player = FirstPersonController(speed=settings['player_speed'], jump_height=settings['player_jump_height'])
player.cursor.color = color.clear
# Add player stamina system
player.stamina = settings['stamina_max']
player.is_sprinting = False
# Set player position above the terrain
player.position = (0, get_height(0, 0) + 100, 0)
sky = Sky(texture='sky.png')

game_sequence_1 = Sequence(Func(render_chunks), Wait(1.5), loop=True)
game_sequence_2 = Sequence(Func(unload_chunks), Wait(1.5), loop=True)
player_stamina_sequence = Sequence(Func(update_stamina), Wait(0.1), loop=True)
player_stress_sequence = Sequence(Func(update_shader_values), loop=True)
player_camera_tilt_sequence = Sequence(Func(update_camera_tilt), Wait(0.01), loop=True)
player_check_y_sequence = Sequence(Func(check_player_y), Wait(5), loop=True)
player_check_y_sequence.start()

print(clr("\n  - Generating first load chunks..."))
first_load()

pause_menu = PauseMenu()
if isinstance(player, FirstPersonController):
    pause_menu.change_camera_mode('Blur Noise')
    player_stamina_sequence.start()
    player_camera_tilt_sequence.start()
if settings['enable_lighting']:
    enable_lighting()
    # enable_filters()
# pause_menu.pause_game()

ambiance_trees = Audio("ambiance_trees.m4a", loop=True, autoplay=True, volume=1)
ambiance_crickets = Audio("ambiance_crickets.m4a", loop=True, autoplay=True, volume=1)

app.run()
