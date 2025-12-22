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
        
        self.speed = 0.6        # Faster than before
        self.turn_speed = 0.2   # Higher = Sharper turns (Smarter missile)
        self.radius = 0.4
        self.alive = True
        
        # Start with random velocity to make them "fan out" slightly before tracking
        self.vx = random.uniform(-0.5, 0.5)
        self.vy = random.uniform(-0.5, 0.5)
        self.vz = -1.0 # Start moving forward strongly

    def update(self):
        # 1. Check if target is still valid
        if self.target and self.target.z > self.z + 5:
             # If target is way behind us, stop tracking
            self.target = None

        # 2. Homing Logic
        if self.target:
            # A. Vector to target
            dx = self.target.x - self.x
            dy = self.target.y - self.y
            dz = self.target.z - self.z
            
            # B. Normalize that vector (Direction only)
            dist = math.sqrt(dx*dx + dy*dy + dz*dz)
            if dist > 0:
                dx /= dist
                dy /= dist
                dz /= dist
                
                # C. STEER: Add target direction to current velocity
                self.vx += dx * self.turn_speed
                self.vy += dy * self.turn_speed
                self.vz += dz * self.turn_speed

        # 3. NORMALIZE VELOCITY (The Fix)
        # This ensures the missile flies at constant speed, 
        # converting the "steering" into a pure direction change.
        v_dist = math.sqrt(self.vx**2 + self.vy**2 + self.vz**2)
        if v_dist > 0:
            self.vx /= v_dist
            self.vy /= v_dist
            self.vz /= v_dist

        # 4. Apply Speed
        self.x += self.vx * self.speed
        self.y += self.vy * self.speed
        self.z += self.vz * self.speed 

        # 5. Cleanup
        if self.z < -200 or self.z > 20:
            self.alive = False

    def draw(self):
        if not self.alive: return
        
        glPushMatrix()
        glTranslatef(self.x, self.y, self.z)
        glScalef(0.3, 0.3, 0.3)
        
        # Draw Diamond Shape
        glBegin(GL_TRIANGLES)
        # Slicing [:3] ensures we only use R,G,B (ignoring the Rainbow Flag if present)
        glColor3fv(self.color[:3])
        
        # Simple Pyramid
        # Top, Front-Right
        glVertex3f(0, 1, 0); glVertex3f(0.5, 0, 0.5); glVertex3f(0.5, 0, -0.5)
        # Top, Front-Left
        glVertex3f(0, 1, 0); glVertex3f(-0.5, 0, 0.5); glVertex3f(-0.5, 0, -0.5)
        # Top, Back-Right
        glVertex3f(0, 1, 0); glVertex3f(0.5, 0, -0.5); glVertex3f(-0.5, 0, -0.5)
        # Bottom Cap (Optional, but makes it solid)
        glVertex3f(0.5, 0, 0.5); glVertex3f(-0.5, 0, 0.5); glVertex3f(0, -1, 0)
        
        glEnd()
        
        glPopMatrix()