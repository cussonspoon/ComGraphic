import random
from OpenGL.GL import *

class Asteroid:
    def __init__(self, start_z=-50.0):
        # --- Geometry (Simple Wireframe Cube for now) ---
        # Later we can randomize these slightly to make it "jagged"
        self.vertices = [
            (-1, -1, -1), (1, -1, -1), (1, 1, -1), (-1, 1, -1), # Back face
            (-1, -1, 1), (1, -1, 1), (1, 1, 1), (-1, 1, 1)      # Front face
        ]
        # Connecting the dots to make a wireframe box
        self.edges = [
            (0,1), (1,2), (2,3), (3,0), # Back square
            (4,5), (5,6), (6,7), (7,4), # Front square
            (0,4), (1,5), (2,6), (3,7)  # Connecting lines
        ]

        # --- Movement Properties ---
        self.x = random.uniform(-6.0, 6.0) # Random horizontal position
        self.y = random.uniform(-4.0, 4.0) # Random vertical position
        self.z = start_z                   # Start far away
        self.speed = random.uniform(0.2, 0.6) # Random forward speed

        # --- Spinning Properties ---
        self.rot_x = 0.0
        self.rot_y = 0.0
        # Random tumbling speeds
        self.rot_speed_x = random.uniform(-3.0, 3.0)
        self.rot_speed_y = random.uniform(-3.0, 3.0)

        # Color (Ready for the future shooter mechanic)
        # Defaulting to Magenta (Red + Blue) for high visibility
        self.color = (1.0, 0.0, 1.0) 

    def update(self):
        # 1. Move forward (towards the camera)
        self.z += self.speed
        
        # 2. Spin
        self.rot_x += self.rot_speed_x
        self.rot_y += self.rot_speed_y

        # 3. Recycle if it passes behind the camera
        # If Z > 5, it's behind us. Send it back to the start.
        if self.z > 5.0:
            self.reset()

    def reset(self):
        """Helper to send the asteroid back to the start with new random stats"""
        self.z = -50.0
        self.x = random.uniform(-6.0, 6.0)
        self.y = random.uniform(-4.0, 4.0)
        self.speed = random.uniform(0.2, 0.6)
        self.rot_speed_x = random.uniform(-3.0, 3.0)
        self.rot_speed_y = random.uniform(-3.0, 3.0)

    def draw(self):
        glPushMatrix()
        # Move to position
        glTranslatef(self.x, self.y, self.z)

        # Spin in place (apply rotation BEFORE drawing)
        glRotatef(self.rot_x, 1, 0, 0) # Rotate around X axis
        glRotatef(self.rot_y, 0, 1, 0) # Rotate around Y axis
        
        # Optional: Scale it slightly randomly for variety
        # glScalef(self.scale, self.scale, self.scale)

        glBegin(GL_LINES)
        glColor3f(self.color[0], self.color[1], self.color[2])
        for e in self.edges:
            for v in e:
                glVertex3fv(self.vertices[v])
        glEnd()
        glPopMatrix()