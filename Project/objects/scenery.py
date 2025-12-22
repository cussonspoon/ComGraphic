from OpenGL.GL import *

class FloorGrid:
    def __init__(self):
        self.y_level = -2.0
        self.scroll_speed = 0.2
        self.z_offset = 0.0
        
    def update(self):
        # Increase offset to simulate forward movement
        self.z_offset += self.scroll_speed

    def draw(self):
        glPushMatrix()
        # Move grid to bottom of screen
        # The modulus (%) creates the infinite loop effect
        glTranslatef(0, self.y_level, (self.z_offset % 5.0)) 
        
        glBegin(GL_LINES)
        glColor3f(0.2, 0.2, 0.2) # Dark Grey
        
        # Draw vertical lines (Z-axis)
        for x in range(-20, 21, 2):
            glVertex3f(x, 0, -50)
            glVertex3f(x, 0, 10)
            
        # Draw horizontal lines (X-axis)
        for z in range(-50, 10, 5):
            glVertex3f(-20, 0, z)
            glVertex3f(20, 0, z)
            
        glEnd()
        glPopMatrix()