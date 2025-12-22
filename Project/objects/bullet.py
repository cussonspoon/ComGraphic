from OpenGL.GL import *

class Bullet:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.speed = 2.0  # Fast speed
        self.radius = 0.2 # Hitbox size
        self.alive = True # False when it hits something or goes off screen

    def update(self):
        # Move forward (into the screen is negative Z)
        self.z -= self.speed
        
        # Despawn if it goes too far
        if self.z < -100.0:
            self.alive = False

    def draw(self):
        glPushMatrix()
        glTranslatef(self.x, self.y, self.z)
        
        glBegin(GL_LINES)
        glColor3f(1.0, 1.0, 0.0) # Yellow Laser
        glVertex3f(0, 0, 0)      # Front
        glVertex3f(0, 0, 2.0)    # Tail (length of bullet)
        glEnd()
        
        glPopMatrix()