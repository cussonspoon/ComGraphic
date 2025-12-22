from OpenGL.GL import *
import math

class WireframeShip:
    def __init__(self):
        # "Viper" Shape
        self.vertices = [
            (0.0, 0.0, -2.0),  # Nose
            (-0.5, 0.0, 0.0), (0.5, 0.0, 0.0), # Wings Start
            (0.0, 0.5, 0.0),   # Cockpit Top
            (-1.5, -0.2, 1.0), (1.5, -0.2, 1.0), # Wing Tips
            (0.0, -0.2, 1.0),  # Engine
            (0.0, 0.5, 1.0),   # Tail
        ]
        
        self.edges = [
            (0,1), (0,2), (0,3), (1,3), (2,3), (1,2),
            (1,4), (4,6), (6,1), (2,5), (5,6), (6,2),
            (3,7), (6,7), (4,5)
        ]
        
        self.x = 0.0
        self.y = 0.0
        self.z = -5.0 # Logic Z
        self.bank_angle = 0.0
        self.sensitivity = 0.01
        
        self.red_on = False
        self.green_on = False
        self.blue_on = False

    def get_current_color(self):
        r = 1.0 if self.red_on else 0.0
        g = 1.0 if self.green_on else 0.0
        b = 1.0 if self.blue_on else 0.0
        if r == 0 and g == 0 and b == 0:
            return (1.0, 1.0, 1.0)
        return (r, g, b)

    def update(self, mouse_dx, mouse_dy):
        self.x += mouse_dx * self.sensitivity
        self.y -= mouse_dy * self.sensitivity
        self.x = max(-10.0, min(10.0, self.x))
        self.y = max(-6.0, min(6.0, self.y))
        self.bank_angle = self.x / 4.0 

    def draw(self):
        glPushMatrix()
        
        # --- FPS COCKPIT OFFSET ---
        # 1. Move to the ship's world position (so it stays with the camera)
        # 2. Move 'down' (-0.5) so it looks like a dashboard
        # 3. Move 'forward' (-1.5) so the nose sticks out in front of us
        glTranslatef(self.x, self.y - 0.5, -1.5) 
        
        # TILT: We rotate ONLY the model, not the camera, to simulate banking
        glRotatef(-self.bank_angle * 30.0, 0, 0, 1)
        
        # Scale it so it doesn't block the whole screen
        glScalef(0.4, 0.4, 0.4) 

        glBegin(GL_LINES)
        
        current_color = self.get_current_color()
        glColor3f(current_color[0], current_color[1], current_color[2])
        
        for e in self.edges:
            for v in e:
                glVertex3fv(self.vertices[v])
        glEnd()
        glPopMatrix()