import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math

# ---------------- Vector helpers ----------------
def normalize(v):
    length = math.sqrt(sum(x*x for x in v))
    if length == 0:
        return [0, 0, 0]
    return [x/length for x in v]

def dot(a, b):
    return sum(x*y for x, y in zip(a, b))

def subtract(a, b):
    return [a[i] - b[i] for i in range(3)]

def add(a, b):
    return [a[i] + b[i] for i in range(3)]

# ---------------- Lighting parameters ----------------
light_pos = [2.0, 2.0, 2.0]
camera_pos = [0.0, 0.0, 5.0]

kd = 0.8     # diffuse coefficient
ks = 0.5     # specular coefficient
p  = 50      # shininess

# ---------------- Rotation parameters (NEW) ----------------
rotation_x = 0.0
rotation_y = 0.0
mouse_dragging = False
last_mouse_x = 0
last_mouse_y = 0

# ---------------- Shading function ----------------
def compute_color(position, normal):
    # Light vector
    l = normalize(subtract(light_pos, position))

    # View vector
    v = normalize(subtract(camera_pos, position))

    # Lambertian diffuse
    diff = max(0.0, dot(normal, l))
    diffuse = kd * diff

    # Blinn-Phong specular
    h = normalize(add(l, v))
    spec = ks * (max(0.0, dot(normal, h)) ** p)

    intensity = diffuse + spec
    return [intensity, intensity, intensity]

# ---------------- Cube data ----------------
vertices = [
    [-1, -1, -1],  # 0
    [ 1, -1, -1],  # 1
    [ 1,  1, -1],  # 2
    [-1,  1, -1],  # 3
    [-1, -1,  1],  # 4
    [ 1, -1,  1],  # 5
    [ 1,  1,  1],  # 6
    [-1,  1,  1],  # 7
]

faces = [
    [4, 5, 6, 7],  # Front
    [0, 3, 2, 1],  # Back
    [0, 4, 7, 3],  # Left
    [1, 2, 6, 5],  # Right
    [3, 7, 6, 2],  # Top
    [0, 1, 5, 4],  # Bottom
]

normals = [
    [ 0,  0,  1],  # Front
    [ 0,  0, -1],  # Back
    [-1,  0,  0],  # Left
    [ 1,  0,  0],  # Right
    [ 0,  1,  0],  # Top
    [ 0, -1,  0],  # Bottom
]

# ---------------- Draw shaded cube ----------------
def draw_cube():
    """Draw cube with per-vertex shading (Lab 7.4 style)"""
    
    for i, face in enumerate(faces):
        face_normal = normals[i]
        
        glBegin(GL_QUADS)
        
        for vertex_index in face:
            # Get vertex position
            pos = vertices[vertex_index]
            
            # Use face normal (flat shading approach)
            # Calculate color based on vertex position
            color = compute_color(pos, face_normal)
            
            # Set color for this vertex
            glColor3fv(color)
            
            # Draw vertex
            glVertex3fv(pos)
        
        glEnd()

# ---------------- Main ----------------
pygame.init()
screen = pygame.display.set_mode((800, 600), DOUBLEBUF | OPENGL)
pygame.display.set_caption("Lab 7.5 - Cube with Mouse Rotation")

gluPerspective(45, 800/600, 0.1, 50.0)
glTranslatef(0, 0, -5)

glEnable(GL_DEPTH_TEST)

clock = pygame.time.Clock()
running = True

print("Lab 7.5 - Cube Shading with Mouse Rotation")
print("Controls:")
print("  Mouse Drag: Rotate cube")
print("  Arrow Keys: Move light X/Z")
print("  W/S: Move light Y (up/down)")
print("  R: Reset rotation (NEW)")
print("  ESC: Quit")

while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
            # Reset rotation (NEW)
            if event.key == K_r:
                rotation_x = 0.0
                rotation_y = 0.0
                print("Rotation reset")
        
        # Mouse button events (NEW)
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                mouse_dragging = True
                last_mouse_x, last_mouse_y = event.pos
        
        if event.type == MOUSEBUTTONUP:
            if event.button == 1:
                mouse_dragging = False
        
        # Mouse motion (NEW)
        if event.type == MOUSEMOTION:
            if mouse_dragging:
                mouse_x, mouse_y = event.pos
                dx = mouse_x - last_mouse_x
                dy = mouse_y - last_mouse_y
                
                # Update rotation angles
                rotation_y += dx * 0.5  # Horizontal mouse movement -> Y-axis rotation
                rotation_x += dy * 0.5  # Vertical mouse movement -> X-axis rotation
                
                last_mouse_x = mouse_x
                last_mouse_y = mouse_y

    # -------- Keyboard light control --------
    keys = pygame.key.get_pressed()
    if keys[K_LEFT]:  light_pos[0] -= 0.05
    if keys[K_RIGHT]: light_pos[0] += 0.05
    if keys[K_UP]:    light_pos[2] -= 0.05
    if keys[K_DOWN]:  light_pos[2] += 0.05
    if keys[K_w]:     light_pos[1] += 0.05
    if keys[K_s]:     light_pos[1] -= 0.05

    # -------- Rendering --------
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    
    glPushMatrix()  # Save current matrix
    glRotatef(rotation_x, 1, 0, 0)  # Rotate around X-axis
    glRotatef(rotation_y, 0, 1, 0)  # Rotate around Y-axis
    
    draw_cube()
    
    glPopMatrix()  # Restore matrix
    
    pygame.display.flip()

pygame.quit()