from OpenGL.GL import *
import math

class WireframeShip:
    def __init__(self):
        # A "Viper" style shape: Long nose, wings at back
        self.vertices = [
            (0.0, 0.0, -2.0),  # 0. Tip
            (-0.5, 0.0, 0.0),  # 1. Left Wing Start
            (0.5, 0.0, 0.0),   # 2. Right Wing Start
            (0.0, 0.5, 0.0),   # 3. Cockpit Top
            (-1.5, -0.2, 1.0), # 4. Left Wing Tip
            (1.5, -0.2, 1.0),  # 5. Right Wing Tip
            (0.0, -0.2, 1.0),  # 6. Engine Center
            (0.0, 0.5, 1.0),   # 7. Tail Fin Top
        ]
        
        self.edges = [
            (0,1), (0,2), (0,3), (1,3), (2,3), (1,2), # Nose
            (1,4), (4,6), (6,1), # Left Wing
            (2,5), (5,6), (6,2), # Right Wing
            (3,7), (6,7), (4,5)  # Tail
        ]
        
        self.x = 0.0
        self.y = 0.0
        self.z = -5.0
        self.bank_angle = 0.0
        self.sensitivity = 0.01

    def update(self, mouse_dx, mouse_dy):
        # 1. Update Position
        self.x += mouse_dx * self.sensitivity
        self.y -= mouse_dy * self.sensitivity
        
        # 2. Clamp to screen edges
        self.x = max(-4.0, min(4.0, self.x))
        self.y = max(-3.0, min(3.0, self.y))
        
        # 3. Calculate Banking (Tilt)
        # We tilt based on X position to simulate "leaning" into the turn
        self.bank_angle = self.x / 4.0 

    def draw(self):
        glPushMatrix()
        glTranslatef(self.x, self.y, -5.0) 
        
        # Apply Banking Rotation
        glRotatef(-self.bank_angle * 30.0, 0, 0, 1)
        
        glBegin(GL_LINES)
        glColor3f(0.0, 1.0, 1.0) # Cyan
        for e in self.edges:
            for v in e:
                glVertex3fv(self.vertices[v])
        glEnd()
        glPopMatrix()