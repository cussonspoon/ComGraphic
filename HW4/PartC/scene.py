import math
from OpenGL.GL import *
from objects import SphereObject

class Scene:
    def __init__(self):
        self.objects = []
        self.floor_texture = None

    def add_object(self, obj):
        self.objects.append(obj)

    def draw(self, camera_pos):
        # 1. Draw Opaque Objects First
        opaque_objs = [o for o in self.objects if not o.is_transparent()]
        for obj in opaque_objs:
            obj.draw()

        # 2. Draw Floor (Opaque)
        if self.floor_texture:
            self.draw_floor()

        # 3. Sort and Draw Transparent Objects (Back-to-Front)
        transp_objs = [o for o in self.objects if o.is_transparent()]
        
        # Sort key: Distance from camera to object center (descending)
        transp_objs.sort(key=lambda o: self.dist_sq(camera_pos, o.pos), reverse=True)

        # Enable blending and disable depth writing for transparency
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glDepthMask(GL_FALSE) # Read-only depth buffer

        for obj in transp_objs:
            obj.draw()

        glDepthMask(GL_TRUE)
        glDisable(GL_BLEND)

    def draw_floor(self):
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.floor_texture)
        
        # --- FIX: RESET COLOR TO WHITE ---
        # This ensures the floor is not tinted by the last drawn object's color
        glColor3f(1.0, 1.0, 1.0) 
        # ---------------------------------

        glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, (1.0, 1.0, 1.0, 1.0))
        glMaterialfv(GL_FRONT, GL_SPECULAR, (0.0, 0.0, 0.0, 1.0))
        
        s = 60.0
        t = 10.0
        y = 0.0
        
        glBegin(GL_QUADS)
        glNormal3f(0.0, 1.0, 0.0)
        glTexCoord2f(0.0, 0.0); glVertex3f(-s, y, -s)
        glTexCoord2f(t, 0.0);   glVertex3f( s, y, -s)
        glTexCoord2f(t, t);     glVertex3f( s, y,  s)
        glTexCoord2f(0.0, t);   glVertex3f(-s, y,  s)
        glEnd()
        
        glBindTexture(GL_TEXTURE_2D, 0)
        glDisable(GL_TEXTURE_2D)

    def dist_sq(self, p1, p2):
        return (p1[0]-p2[0])**2 + (p1[1]-p2[1])**2 + (p1[2]-p2[2])**2