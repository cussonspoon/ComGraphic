import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image
import math
import random  # Added for random object generation

# Import our modules
from objects import SphereObject
from scene import Scene
from picking import get_ray_from_mouse, ray_sphere_intersect
from io_scene import save_scene, load_scene

# Config
WIN_W, WIN_H = 1024, 768
FPS = 60

# Camera
camera_target = [0.0, 0.0, 0.0]
camera_yaw = 0.0
camera_pitch = 20.0
camera_dist = 20.0

# Mouse State
last_mouse = None
orbiting = False
panning = False

# Light
light_pos = [5.0, 5.0, 5.0, 1.0]

# Modes
MODE_CAMERA = 0
MODE_LIGHT = 1
current_mode = MODE_CAMERA

# Selected Object
selected_obj = None

def load_texture(path):
    try:
        img = Image.open(path).convert("RGB")
        img = img.transpose(Image.FLIP_TOP_BOTTOM)
        data = img.tobytes()
        
        tex = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, tex)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img.width, img.height, 0, GL_RGB, GL_UNSIGNED_BYTE, data)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        return tex
    except:
        print(f"Texture {path} not found. Floor will be white.")
        return 0

# --- Math Helpers for Camera ---
def normalize(v):
    l = math.sqrt(v[0]**2 + v[1]**2 + v[2]**2)
    if l == 0: return [0,0,0]
    return [v[0]/l, v[1]/l, v[2]/l]

def cross(a, b):
    return [
        a[1]*b[2] - a[2]*b[1],
        a[2]*b[0] - a[0]*b[2],
        a[0]*b[1] - a[1]*b[0],
    ]

def get_camera_vectors():
    """Returns eye position, right vector, and up vector for panning."""
    ry = math.radians(camera_yaw)
    rp = math.radians(camera_pitch)
    
    # Calculate Eye Position
    eye = [
        camera_target[0] + camera_dist * math.cos(rp) * math.sin(ry),
        camera_target[1] + camera_dist * math.sin(rp),
        camera_target[2] + camera_dist * math.cos(rp) * math.cos(ry),
    ]

    # Calculate Basis Vectors (Right and Up)
    forward = [camera_target[0] - eye[0], camera_target[1] - eye[1], camera_target[2] - eye[2]]
    forward = normalize(forward)
    
    world_up = [0.0, 1.0, 0.0]
    right = normalize(cross(forward, world_up))
    up = normalize(cross(right, forward))
    
    return eye, right, up

def handle_picking(x, y, scene):
    global selected_obj
    ray_origin, ray_dir = get_ray_from_mouse(x, y)
    
    if not ray_origin: return

    closest_dist = float('inf')
    hit_obj = None

    for obj in scene.objects:
        if isinstance(obj, SphereObject):
            dist = ray_sphere_intersect(ray_origin, ray_dir, obj.pos, obj.radius)
            if dist is not None and dist < closest_dist:
                closest_dist = dist
                hit_obj = obj
    
    if selected_obj: selected_obj.selected = False
    selected_obj = hit_obj
    if selected_obj: selected_obj.selected = True

def main():
    global camera_yaw, camera_pitch, camera_dist, camera_target
    global last_mouse, orbiting, panning, current_mode, light_pos, selected_obj

    pygame.init()
    screen = pygame.display.set_mode((WIN_W, WIN_H), DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Challenge HW: Interactive Scene Editor")

    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_NORMALIZE)
    glEnable(GL_COLOR_MATERIAL)
    glShadeModel(GL_SMOOTH)
    glClearColor(0.1, 0.1, 0.1, 1.0)

    main_scene = Scene()
    main_scene.floor_texture = load_texture("floor.jpg")

    # --- Initial Objects ---
    # Red (Opaque), Green (Transparent 0.5), Blue (Transparent 0.5)
    main_scene.add_object(SphereObject(-3, 1, 0, 1.0, 1, 0, 0, 1.0)) 
    main_scene.add_object(SphereObject(0, 1, 0, 1.0, 0, 1, 0, 0.5))  
    main_scene.add_object(SphereObject(3, 1, 0, 1.0, 0, 0, 1, 0.5))  

    clock = pygame.time.Clock()

    while True:
        # 1. Event Handling
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit(); return
            
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE: pygame.quit(); return
                
                # Mode Switching
                if event.key == K_TAB:
                    current_mode = MODE_LIGHT if current_mode == MODE_CAMERA else MODE_CAMERA
                
                # Save/Load
                mods = pygame.key.get_mods()
                if (mods & KMOD_CTRL):
                    if event.key == K_s: save_scene(main_scene)
                    if event.key == K_l: load_scene(main_scene)

                # --- NEW: ADD RANDOM OBJECT (Press 'A') ---
                if event.key == K_a:
                    rx = random.uniform(-5, 5)
                    rz = random.uniform(-5, 5)
                    rr, rg, rb = random.random(), random.random(), random.random()
                    # 50% chance of being transparent
                    ra = 0.5 if random.random() > 0.5 else 1.0
                    
                    new_obj = SphereObject(rx, 1, rz, 1.0, rr, rg, rb, ra)
                    main_scene.add_object(new_obj)
                    print(f"Added sphere at {rx:.2f}, {rz:.2f} (Alpha: {ra})")

            # --- MOUSE INPUTS ---
            if event.type == MOUSEBUTTONDOWN:
                mods = pygame.key.get_mods()
                shift = (mods & KMOD_SHIFT)

                # Zoom In/Out (Scroll Wheel)
                if event.button == 4: camera_dist = max(2.0, camera_dist - 1.0)
                if event.button == 5: camera_dist = min(100.0, camera_dist + 1.0)

                # Left Click logic
                if event.button == 1:
                    if shift:
                        panning = True
                    else:
                        orbiting = True
                        # Only pick if we are NOT panning
                        if current_mode == MODE_CAMERA:
                             handle_picking(event.pos[0], event.pos[1], main_scene)

            if event.type == MOUSEBUTTONUP:
                if event.button == 1:
                    orbiting = False
                    panning = False

        # 2. Continuous Input (Keyboard)
        keys = pygame.key.get_pressed()
        shift_held = keys[K_LSHIFT] or keys[K_RSHIFT]
        move_speed = 0.05 if shift_held else 0.2

        if current_mode == MODE_LIGHT:
            if keys[K_UP]: light_pos[2] -= 0.2
            if keys[K_DOWN]: light_pos[2] += 0.2
            if keys[K_LEFT]: light_pos[0] -= 0.2
            if keys[K_RIGHT]: light_pos[0] += 0.2
            if keys[K_q]: light_pos[1] += 0.2
            if keys[K_e]: light_pos[1] -= 0.2

        if selected_obj:
            if keys[K_i]: selected_obj.pos[2] -= move_speed
            if keys[K_k]: selected_obj.pos[2] += move_speed
            if keys[K_j]: selected_obj.pos[0] -= move_speed
            if keys[K_l]: selected_obj.pos[0] += move_speed
            if keys[K_u]: selected_obj.pos[1] += move_speed
            if keys[K_o]: selected_obj.pos[1] -= move_speed

        # 3. Mouse Motion (Orbit / Pan)
        mx, my = pygame.mouse.get_pos()
        if last_mouse:
            dx = mx - last_mouse[0]
            dy = my - last_mouse[1]

            if panning:
                eye, right, up = get_camera_vectors()
                pan_speed = 0.01 * (camera_dist / 10.0)
                
                # Pan target
                camera_target[0] -= right[0] * dx * pan_speed
                camera_target[1] -= right[1] * dx * pan_speed
                camera_target[2] -= right[2] * dx * pan_speed
                
                camera_target[0] += up[0] * dy * pan_speed
                camera_target[1] += up[1] * dy * pan_speed
                camera_target[2] += up[2] * dy * pan_speed

            elif orbiting:
                camera_yaw += dx * 0.3
                camera_pitch -= dy * 0.3
                camera_pitch = max(-89, min(89, camera_pitch))

        last_mouse = (mx, my)

        # 4. Rendering
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, (WIN_W / WIN_H), 0.1, 100.0)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        
        # Recalculate eye for gluLookAt
        eye, _, _ = get_camera_vectors()
        gluLookAt(eye[0], eye[1], eye[2], 
                  camera_target[0], camera_target[1], camera_target[2], 
                  0, 1, 0)

        glLightfv(GL_LIGHT0, GL_POSITION, light_pos)
        main_scene.draw(eye)

        mode_str = "LIGHT MODE (Arrows=XZ, Q/E=Y)" if current_mode == MODE_LIGHT else "CAMERA MODE (Shift+Drag=Pan)"
        pygame.display.set_caption(f"HW Editor | {mode_str} | Light: {light_pos[0]:.1f},{light_pos[1]:.1f},{light_pos[2]:.1f} | 'A' to Add")

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()