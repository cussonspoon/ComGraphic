from OpenGL.GL import *

class Bullet:
    # 1. Added 'color' parameter
    def __init__(self, x, y, z, color):
        self.x = x
        self.y = y
        self.z = z
        self.color = color   # Store the color (r, g, b)
        self.speed = 2.0
        self.radius = 0.2
        self.alive = True

    def update(self):
        self.z -= self.speed
        if self.z < -100.0:
            self.alive = False

    def draw(self):
        glPushMatrix()
        glTranslatef(self.x, self.y, self.z)
        
        glBegin(GL_LINES)
        # 2. Use the stored color instead of hardcoded Yellow
        glColor3fv(self.color[:3])
        
        glVertex3f(0, 0, 0)
        glVertex3f(0, 0, 2.0)
        glEnd()
        
        glPopMatrix()