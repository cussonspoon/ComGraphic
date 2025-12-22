import random
import math
from OpenGL.GL import *

class Missile:
    def __init__(self, x, y, z, target_asteroid, color):
        self.x = x
        self.y = y
        self.z = z
        self.target = target_asteroid
        self.color = color
        
        self.speed = 0.6
        self.turn_speed = 0.2
        self.radius = 0.4
        self.alive = True
        
        # Start with random velocity
        self.vx = random.uniform(-0.5, 0.5)
        self.vy = random.uniform(-0.5, 0.5)
        self.vz = -1.0 

    def update(self):
        # 1. Check Target
        if self.target and self.target.z > self.z + 5:
            self.target = None

        # 2. Homing Steering
        if self.target:
            dx = self.target.x - self.x
            dy = self.target.y - self.y
            dz = self.target.z - self.z
            
            dist = math.sqrt(dx*dx + dy*dy + dz*dz)
            if dist > 0:
                dx /= dist; dy /= dist; dz /= dist
                self.vx += dx * self.turn_speed
                self.vy += dy * self.turn_speed
                self.vz += dz * self.turn_speed

        # 3. Normalize Speed (Constant Velocity)
        v_dist = math.sqrt(self.vx**2 + self.vy**2 + self.vz**2)
        if v_dist > 0:
            self.vx /= v_dist
            self.vy /= v_dist
            self.vz /= v_dist

        # 4. Move
        self.x += self.vx * self.speed
        self.y += self.vy * self.speed
        self.z += self.vz * self.speed 

        if self.z < -200 or self.z > 20:
            self.alive = False

    def draw(self):
        if not self.alive: return
        
        glPushMatrix()
        glTranslatef(self.x, self.y, self.z)
        glScalef(0.3, 0.3, 0.3)
        
        # --- CHANGED TO WIREFRAME (GL_LINES) ---
        glBegin(GL_LINES)
        glColor3fv(self.color[:3]) # Safety slice for color
        
        # Vertices for a Diamond (Octahedron)
        top = (0, 1, 0)
        bot = (0, -1, 0)
        p1 = (0.5, 0, 0.5)
        p2 = (0.5, 0, -0.5)
        p3 = (-0.5, 0, -0.5)
        p4 = (-0.5, 0, 0.5)
        
        # 1. Connect Top to Middle Ring
        glVertex3fv(top); glVertex3fv(p1)
        glVertex3fv(top); glVertex3fv(p2)
        glVertex3fv(top); glVertex3fv(p3)
        glVertex3fv(top); glVertex3fv(p4)
        
        # 2. Connect Bottom to Middle Ring
        glVertex3fv(bot); glVertex3fv(p1)
        glVertex3fv(bot); glVertex3fv(p2)
        glVertex3fv(bot); glVertex3fv(p3)
        glVertex3fv(bot); glVertex3fv(p4)
        
        # 3. Connect Middle Ring together
        glVertex3fv(p1); glVertex3fv(p2)
        glVertex3fv(p2); glVertex3fv(p3)
        glVertex3fv(p3); glVertex3fv(p4)
        glVertex3fv(p4); glVertex3fv(p1)
        
        glEnd()
        glPopMatrix()