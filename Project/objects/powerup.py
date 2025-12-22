import math
import random
from OpenGL.GL import *

class PowerUp:
    def __init__(self):
        # Position
        self.x = random.uniform(-5, 5)
        self.y = random.uniform(-3, 3)
        self.z = -100.0 # Start far away
        
        self.speed = 0.3
        self.radius = 0.5 # Hitbox size
        self.alive = True
        
        # Scaling Animation vars
        self.scale = 1.0
        self.pulse_timer = 0.0 # Replaces angle for rotation

    def update(self):
        self.z += self.speed
        
        # PULSE ANIMATION (Scaling only)
        # We increment a timer to drive the Sine wave
        self.pulse_timer += 0.1
        # Scale oscillates between roughly 0.8 and 1.2
        self.scale = 1.0 + (math.sin(self.pulse_timer) * 0.2)

        # Reset if it passes the camera
        if self.z > 5.0:
            self.reset()

    def reset(self):
        self.z = -100.0 - random.randint(0, 50)
        self.x = random.uniform(-5, 5)
        self.y = random.uniform(-3, 3)
        self.alive = True

    def draw(self):
        if not self.alive: return
        
        glPushMatrix()
        glTranslatef(self.x, self.y, self.z)
        
        # Apply the Pulsing Scale
        glScalef(self.scale, self.scale, self.scale) 
        
        # --- 1. DRAW THE BOX (Border) ---
        glColor3f(1.0, 1.0, 1.0) # White Box
        glBegin(GL_LINE_LOOP)
        glVertex3f(-0.5, 0.5, 0)  # Top Left
        glVertex3f(0.5, 0.5, 0)   # Top Right
        glVertex3f(0.5, -0.5, 0)  # Bottom Right
        glVertex3f(-0.5, -0.5, 0) # Bottom Left
        glEnd()

        # --- 2. DRAW THE HEART (Icon) ---
        glColor3f(1.0, 0.0, 0.0) # Red Heart
        glBegin(GL_LINE_LOOP)
        # Bottom Tip
        glVertex3f(0.0, -0.3, 0)
        # Right Side
        glVertex3f(0.2, 0.0, 0)
        glVertex3f(0.2, 0.2, 0)
        glVertex3f(0.1, 0.3, 0)
        # Center Dip
        glVertex3f(0.0, 0.1, 0)
        # Left Side
        glVertex3f(-0.1, 0.3, 0)
        glVertex3f(-0.2, 0.2, 0)
        glVertex3f(-0.2, 0.0, 0)
        glEnd()
        
        glPopMatrix()