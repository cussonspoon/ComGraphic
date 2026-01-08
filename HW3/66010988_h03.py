import sys
import math
import os
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

WIDTH, HEIGHT = 800, 600
OFFSET_FIX = 2.0  

class Snowman:
    def __init__(self, filename):
        self.vertices = []
        self.normals = []
        self.faces = []
        self.materials = {}
        
        self.load_materials(filename)
        
        try:
            for line in open(filename, "r"):
                if line.startswith('#'): continue
                values = line.split()
                if not values: continue
                
                if values[0] == 'v':
                    self.vertices.append(list(map(float, values[1:4])))
                elif values[0] == 'vn':
                    self.normals.append(list(map(float, values[1:4])))
                elif values[0] == 'usemtl':
                    self.current_material = values[1]
                elif values[0] == 'f':
                    face_data = []
                    for v in values[1:]:
                        w = v.split('/')
                        vertex_idx = int(w[0]) - 1
                        if len(w) >= 3 and len(w[2]) > 0:
                            normal_idx = int(w[2]) - 1
                        else:
                            normal_idx = -1
                        face_data.append((vertex_idx, normal_idx))
                    self.faces.append((face_data, getattr(self, 'current_material', None)))
                    
        except IOError:
            print(f"ERROR: Could not find {filename}.")
            sys.exit()

    def load_materials(self, obj_filename):
        mtl_filename = obj_filename.replace(".obj", ".mtl")
        if not os.path.exists(mtl_filename):
            print(f"Warning: {mtl_filename} not found.")
            return

        current_mtl_name = None
        for line in open(mtl_filename, "r"):
            if line.startswith("newmtl"):
                current_mtl_name = line.split()[1]
            elif line.startswith("Kd"):
                color = list(map(float, line.split()[1:4]))
                color.append(1.0) 
                if current_mtl_name:
                    self.materials[current_mtl_name] = color

    def render(self):
        glBegin(GL_TRIANGLES)
        current_drawn_mat = None
        default_color = [1.0, 1.0, 1.0, 1.0]
        
        for face_data, material_name in self.faces:
            if material_name != current_drawn_mat:
                current_drawn_mat = material_name
                if material_name and material_name in self.materials:
                    glMaterialfv(GL_FRONT, GL_DIFFUSE, self.materials[material_name])
                else:
                    glMaterialfv(GL_FRONT, GL_DIFFUSE, default_color)

            for vertex_idx, normal_idx in face_data:
                if normal_idx >= 0:
                    glNormal3fv(self.normals[normal_idx])
                glVertex3fv(self.vertices[vertex_idx])
        glEnd()

def init_pygame():
    pygame.init()
    pygame.display.set_mode((WIDTH, HEIGHT), DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Press 'D' to Dance")

def init_opengl():
    glClearColor(0.5, 0.7, 1.0, 1.0) 
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_CULL_FACE)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    
    glLightfv(GL_LIGHT0, GL_POSITION, [10.0, 10.0, 10.0, 1.0])
    glLightfv(GL_LIGHT0, GL_DIFFUSE,  [1.0, 1.0, 1.0, 1.0])
    glLightfv(GL_LIGHT0, GL_SPECULAR, [0.2, 0.2, 0.2, 1.0])

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60.0, WIDTH / float(HEIGHT), 0.1, 100.0)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    

    gluLookAt(0.0, 0.0, 9.0, 
              0.0, 0.5, 0.0,   
              0.0, 1.0, 0.0)   

def main():
    init_pygame()
    init_opengl()

    snowman = Snowman("snowman.obj") 

    clock = pygame.time.Clock()

    is_dancing = False
    dance_timer = 0.0
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                if event.key == K_d:
                    is_dancing = True
                    dance_timer = 0.0

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glPushMatrix()

        glRotatef(180, 0, 1, 0) 

        #Dance Animation
        if is_dancing:
            dance_timer += 0.1 
            jump_height = abs(math.sin(dance_timer)) * 1.5
            spin_angle = dance_timer * 50.0 

            glTranslatef(0.0, jump_height, 0.0) 
            glRotatef(spin_angle, 0.0, 1.0, 0.0) 

            if dance_timer > 6.28: 
                is_dancing = False
                dance_timer = 0.0


        glTranslatef(0.0, OFFSET_FIX, 0.0)
        
        snowman.render()

        glPopMatrix()

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()