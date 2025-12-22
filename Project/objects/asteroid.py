import random
from OpenGL.GL import *

class Asteroid:
    def __init__(self, start_z=-50.0):
        # --- Geometry (Wireframe Cube) ---
        self.vertices = [
            (-1, -1, -1), (1, -1, -1), (1, 1, -1), (-1, 1, -1),
            (-1, -1, 1), (1, -1, 1), (1, 1, 1), (-1, 1, 1)
        ]
        self.edges = [
            (0,1), (1,2), (2,3), (3,0),
            (4,5), (5,6), (6,7), (7,4),
            (0,4), (1,5), (2,6), (3,7)
        ]

        # --- Movement Properties ---
        self.x = 0
        self.y = 0
        self.z = start_z
        
        self.speed = random.uniform(0.1, 0.3) 

        self.rot_x = 0.0
        self.rot_y = 0.0
        self.rot_speed_x = random.uniform(-3.0, 3.0)
        self.rot_speed_y = random.uniform(-3.0, 3.0)

        # --- COLORS ---
        self.POSSIBLE_COLORS = [
            (1.0, 0.0, 0.0), # Red
            (0.0, 1.0, 0.0), # Green
            (0.0, 0.0, 1.0), # Blue
            (1.0, 1.0, 0.0), # Yellow
            (0.0, 1.0, 1.0), # Cyan
            (1.0, 0.0, 1.0), # Magenta
            (1.0, 1.0, 1.0)  # White
        ]
        self.color = (1.0, 1.0, 1.0) # Default
        self.reset(full_reset=True)

    def update(self):
        self.z += self.speed
        self.rot_x += self.rot_speed_x
        self.rot_y += self.rot_speed_y

        if self.z > 5.0:
            self.reset()

    def reset(self, full_reset=False):
        if full_reset:
            self.z = -50.0
        else:
            self.z = -100.0 
            
        self.x = random.uniform(-6.0, 6.0)
        self.y = random.uniform(-4.0, 4.0)
        self.speed = random.uniform(0.1, 0.3)
        self.color = random.choice(self.POSSIBLE_COLORS)

    # --- UPDATED DRAW METHOD ---
    def draw(self, is_invincible=False):
        glPushMatrix()
        glTranslatef(self.x, self.y, self.z)
        glRotatef(self.rot_x, 1, 0, 0)
        glRotatef(self.rot_y, 0, 1, 0)
        
        glBegin(GL_LINES)
        
        # VISUAL CUE: If invincible, use Grey. Otherwise, use normal color.
        if is_invincible:
            glColor3f(0.5, 0.5, 0.5) # Grey
        else:
            glColor3f(self.color[0], self.color[1], self.color[2])
            
        for e in self.edges:
            for v in e:
                glVertex3fv(self.vertices[v])
        glEnd()
        glPopMatrix()