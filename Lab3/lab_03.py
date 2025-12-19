import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import math

# --- GLOBAL STATE ---
current_shape = 'cube'  # cube, pyramid, sphere
scale_val = 1.0
angle_y = 0.0
pos_x = 0.0
pos_z = -5.0  # Start a bit back so we can see it

# --- 1. MANUAL MATRIX DEFINITIONS ---

def get_translation_matrix(tx, ty, tz):
    return np.array([
        [1, 0, 0, tx],
        [0, 1, 0, ty],
        [0, 0, 1, tz],
        [0, 0, 0, 1]
    ], dtype=np.float32)

def get_scale_matrix(sx, sy, sz):
    return np.array([
        [sx, 0, 0, 0],
        [0, sy, 0, 0],
        [0, 0, sz, 0],
        [0, 0, 0, 1]
    ], dtype=np.float32)

def get_rotation_y_matrix(degrees):
    rad = math.radians(degrees)
    c = math.cos(rad)
    s = math.sin(rad)
    return np.array([
        [c, 0, s, 0],
        [0, 1, 0, 0],
        [-s, 0, c, 0],
        [0, 0, 0, 1]
    ], dtype=np.float32)

# --- 2. TRANSFORMATION LOGIC ---

def transform_vertices(vertices):
    """
    Applies Scale -> Rotate -> Translate manually to a list of vertices.
    """
    # 1. Create the matrices
    S = get_scale_matrix(scale_val, scale_val, scale_val)
    R = get_rotation_y_matrix(angle_y)
    T = get_translation_matrix(pos_x, 0, pos_z)

    # 2. Combine them: Final = T * R * S
    # (Order matters: Scale first, then Rotate, then Move)
    ModelMatrix = T @ R @ S

    transformed_list = []
    
    for v in vertices:
        # Convert vertex (x,y,z) to homogeneous coordinate (x,y,z,1)
        p = np.array([v[0], v[1], v[2], 1.0])
        
        # Apply Transformation: Matrix * Point
        p_new = ModelMatrix @ p
        
        # Store result (x, y, z)
        transformed_list.append((p_new[0], p_new[1], p_new[2]))
        
    return transformed_list

# --- 3. SHAPE DATA GENERATORS ---

def get_cube_data():
    # Simple Cube Vertices
    vertices = [
        (-1, -1, -1), (1, -1, -1), (1, 1, -1), (-1, 1, -1), # Back face
        (-1, -1, 1), (1, -1, 1), (1, 1, 1), (-1, 1, 1)      # Front face
    ]
    # Indices to draw quads (6 faces)
    faces = [
        (0,1,2,3), (4,5,6,7), (0,1,5,4), (2,3,7,6), (0,3,7,4), (1,2,6,5)
    ]
    return vertices, faces

def get_pyramid_data():
    # Pyramid: 1 top point, 4 base points
    vertices = [
        (0, 1, 0),          # Top
        (-1, -1, 1), (1, -1, 1), (1, -1, -1), (-1, -1, -1) # Base
    ]
    # Indices (4 triangles sides + 1 quad base)
    faces = [
        (0,1,2), (0,2,3), (0,3,4), (0,4,1), # Sides
        (1,2,3,4) # Base
    ]
    return vertices, faces

def get_sphere_data(slices=12, stacks=12):
    # Generating a sphere using latitude/longitude math
    vertices = []
    faces = []
    
    for i in range(stacks + 1):
        lat = math.pi * (-0.5 + float(i) / stacks)
        z = math.sin(lat)
        zr = math.cos(lat)
        
        for j in range(slices + 1):
            lng = 2 * math.pi * float(j) / slices
            x = zr * math.cos(lng)
            y = zr * math.sin(lng)
            vertices.append((x, y, z))
            
    # Generate Quads connecting the vertices
    for i in range(stacks):
        for j in range(slices):
            first = (i * (slices + 1)) + j
            second = first + slices + 1
            faces.append((first, second, second + 1, first + 1))
            
    return vertices, faces

# --- 4. MAIN LOOP ---

def main():
    global current_shape, scale_val, angle_y, pos_x, pos_z
    
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    
    # Camera Perspective (Built-in for the View, but object transforms are manual)
    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
    
    # Enable Depth Buffer so objects look solid
    glEnable(GL_DEPTH_TEST) 

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            
            # KEYBOARD INPUTS
            if event.type == pygame.KEYDOWN:
                # Shape Switching
                if event.key == pygame.K_c: current_shape = 'cube'
                if event.key == pygame.K_p: current_shape = 'pyramid'
                if event.key == pygame.K_s: current_shape = 'sphere'
                
                # Scaling
                if event.key == pygame.K_UP: scale_val += 0.1
                if event.key == pygame.K_DOWN: scale_val = max(0.1, scale_val - 0.1)
                
                # Rotation
                if event.key == pygame.K_LEFT: angle_y -= 5
                if event.key == pygame.K_RIGHT: angle_y += 5
                
                # Movement (Translation)
                if event.key == pygame.K_w: pos_z += 0.5  # Move Forward (technically +z in this cam setup)
                if event.key == pygame.K_s: pos_z -= 0.5
                if event.key == pygame.K_a: pos_x -= 0.5
                if event.key == pygame.K_d: pos_x += 0.5

        # --- RENDER FRAME ---
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        # 1. Get Raw Data
        if current_shape == 'cube':
            raw_verts, faces = get_cube_data()
        elif current_shape == 'pyramid':
            raw_verts, faces = get_pyramid_data()
        else:
            raw_verts, faces = get_sphere_data()

        # 2. MANUALLY TRANSFORM VERTICES (The Core Task)
        # This replaces glTranslate, glRotate, glScale
        final_verts = transform_vertices(raw_verts)

        # 3. Draw Lines/Polygons using the Transformed Vertices
        glBegin(GL_LINES) # Using lines to see the "Wireframe" clearly
        
        for face in faces:
            for i in range(len(face)):
                # Connect current point to next point
                p1 = final_verts[face[i]]
                p2 = final_verts[face[(i+1) % len(face)]]
                
                glVertex3f(p1[0], p1[1], p1[2])
                glVertex3f(p2[0], p2[1], p2[2])
        glEnd()

        pygame.display.flip()
        pygame.time.wait(10)

if __name__ == "__main__":
    main()