import random
from OpenGL.GL import *

class Star:
    def __init__(self):
        # Spread stars out widely
        self.x = random.uniform(-20, 20)
        self.y = random.uniform(-10, 10)
        self.z = random.uniform(-50, -10)
        # Parallax speed (background moves slower than foreground)
        self.speed = 0.05 

    def update(self):
        self.z += self.speed
        # Recycle star if it passes the camera
        if self.z > 0:
            self.z = -50
            self.x = random.uniform(-20, 20)
            self.y = random.uniform(-10, 10)

    def draw(self):
        glPointSize(2) # Make the dots visible
        glBegin(GL_POINTS)
        glColor3f(1.0, 1.0, 1.0) # White
        glVertex3f(self.x, self.y, self.z)
        glEnd()