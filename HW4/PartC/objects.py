import math
from OpenGL.GL import *
from OpenGL.GLU import *

class SceneObject:
    def __init__(self, x, y, z, r, g, b, a=1.0):
        self.pos = [x, y, z]
        self.color = [r, g, b, a]
        self.selected = False
        
    def is_transparent(self):
        # Objects are transparent if Alpha < 1.0
        return self.color[3] < 1.0

    def draw(self):
        raise NotImplementedError("Draw method must be implemented by subclasses")

class SphereObject(SceneObject):
    def __init__(self, x, y, z, radius, r, g, b, a=1.0, shininess=30.0, specular=0.5):
        super().__init__(x, y, z, r, g, b, a)
        self.radius = radius
        self.shininess = shininess
        self.specular = specular
        self.quad = gluNewQuadric()

    def draw(self):
        glPushMatrix()
        glTranslatef(self.pos[0], self.pos[1], self.pos[2])
        
        # --- FIX: Use glColor4f to set color because GL_COLOR_MATERIAL is enabled ---
        # This ensures the Red, Green, and Blue colors actually appear.
        glColor4f(self.color[0], self.color[1], self.color[2], self.color[3])
        
        # Apply Specular/Shininess manually (not handled by Color Material)
        spec_val = self.specular
        glMaterialfv(GL_FRONT, GL_SPECULAR, (spec_val, spec_val, spec_val, 1.0))
        glMaterialf(GL_FRONT, GL_SHININESS, self.shininess)
        
        # Draw Sphere
        gluSphere(self.quad, self.radius, 32, 32)
        
        # Selection Cue: Wireframe Overlay
        if self.selected:
            glDisable(GL_LIGHTING)
            glDisable(GL_TEXTURE_2D)
            glDepthFunc(GL_LEQUAL)
            
            # Draw RED wireframe
            glColor3f(1.0, 0.0, 0.0) 
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
            
            # Draw slightly larger wireframe sphere
            gluSphere(self.quad, self.radius * 1.02, 16, 16)
            
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

            # --- RESET COLOR TO WHITE ---
            # Prevents floor and other objects from getting tinted red
            glColor3f(1.0, 1.0, 1.0)
            
            glEnable(GL_LIGHTING)
            glDepthFunc(GL_LESS)
            
        glPopMatrix()

    def to_dict(self):
        return {
            "type": "sphere",
            "pos": self.pos,
            "radius": self.radius,
            "color": self.color,
            "shininess": self.shininess,
            "specular": self.specular
        }