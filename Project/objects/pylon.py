from OpenGL.GL import *
import random

class ShieldPylon:
    def __init__(self):
        # FIXED POSITION (Non-Movable)
        # Sits in the upper-center background
        self.x = 0.0
        self.y = 5.0
        self.z = -45.0
        
        self.radius = 3.0
        self.active = False      # Starts broken
        self.health = 3          # Takes 3 shots to break
        self.timer = 0           # Timer for random activation
        self.rotation = 0

    def update(self):
        # Strictly Non-Movable (X, Y, Z do not change)
        
        # Rotation animation
        self.rotation += 5.0 if self.active else 1.0

        # Logic: Randomly activate if currently broken
        if not self.active:
            self.timer += 1
            # Every ~5 seconds (300 frames), small chance to activate
            if self.timer > 300 and random.random() < 0.01:
                self.activate()

    def activate(self):
        self.active = True
        self.health = 3 # Reset HP
        print("WARNING: SHIELD PYLON ACTIVATED!")

    def hit(self):
        """Called when player shoots the pylon"""
        if self.active:
            self.health -= 1
            if self.health <= 0:
                self.active = False
                self.timer = 0
                print("SHIELD PYLON DESTROYED!")
                return True # Return True if destroyed
        return False

    def draw(self):
        glPushMatrix()
        glTranslatef(self.x, self.y, self.z)
        glRotatef(self.rotation, 0, 1, 0)
        
        # Scale distinctively
        glScalef(2.0, 4.0, 2.0)
        
        # COLOR LOGIC
        if self.active:
            # Bright White/Cyan (Shielding)
            glColor3f(0.8, 1.0, 1.0)
            glLineWidth(2.0)
        else:
            # Dark Grey (Broken/Offline)
            glColor3f(0.2, 0.2, 0.2)
            glLineWidth(1.0)
        
        # Draw "Tower" Shape (Wireframe)
        glBegin(GL_LINES)
        
        # Base to Tip
        tips = [(1,0,1), (1,0,-1), (-1,0,-1), (-1,0,1)]
        top = (0, 1, 0)
        bottom = (0, -1, 0)
        
        for t in tips:
            # Connect to Top
            glVertex3fv(top); glVertex3fv(t)
            # Connect to Bottom
            glVertex3fv(bottom); glVertex3fv(t)
            # Connect to adjacent (Ring)
            # (Simplified for brevity, just vertical lines is enough for a pylon look)
            
        # Draw a central core line
        glVertex3f(0, 1.5, 0); glVertex3f(0, -1.5, 0)
        
        glEnd()
        glLineWidth(1.0)
        glPopMatrix()