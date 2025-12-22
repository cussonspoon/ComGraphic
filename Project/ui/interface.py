import pygame
from OpenGL.GL import *
from OpenGL.GLU import *

class Interface:
    def __init__(self):
        pygame.font.init()
        self.font = pygame.font.SysFont("Arial", 32, bold=True)
        self.text_color = (255, 255, 255, 255)

    def draw_text_gl(self, x, y, text_string):
        text_surface = self.font.render(text_string, True, self.text_color, (0, 0, 0, 0))
        text_data = pygame.image.tostring(text_surface, "RGBA", True)
        width, height = text_surface.get_width(), text_surface.get_height()
        glRasterPos2i(x, y)
        glDrawPixels(width, height, GL_RGBA, GL_UNSIGNED_BYTE, text_data)

    def draw(self, display_size, score, lives):
        width, height = display_size

        # --- 1. Switch to 2D ---
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        gluOrtho2D(0, width, 0, height)
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()
        
        glDisable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        # --- 2. Draw Text (No Crosshair) ---
        self.draw_text_gl(10, height - 40, f"Score: {score}")
        self.draw_text_gl(10, height - 80, f"Lives: {lives}")

        # --- 3. Restore 3D ---
        glDisable(GL_BLEND)
        glEnable(GL_DEPTH_TEST)
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
        glPopMatrix()