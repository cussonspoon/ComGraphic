import pygame
from OpenGL.GL import *
from OpenGL.GLU import *

class Interface:
    def __init__(self):
        pygame.font.init()
        # Use default system font, size 32
        self.font = pygame.font.SysFont("Arial", 32, bold=True)
        self.text_color = (255, 255, 255, 255) # White

    def draw_text_gl(self, x, y, text_string):
        """Helper to render text in OpenGL"""
        text_surface = self.font.render(text_string, True, self.text_color, (0, 0, 0, 0))
        text_data = pygame.image.tostring(text_surface, "RGBA", True)
        width, height = text_surface.get_width(), text_surface.get_height()
        glRasterPos2i(x, y)
        glDrawPixels(width, height, GL_RGBA, GL_UNSIGNED_BYTE, text_data)

    def draw(self, display_size, score, lives):
        width, height = display_size
        
        # Calculate Center of Screen
        cx, cy = width // 2, height // 2

        # --- 1. Switch to 2D Overlay Mode ---
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        gluOrtho2D(0, width, 0, height) # 0,0 is bottom-left
        
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()
        
        glDisable(GL_DEPTH_TEST) # Draw on top of everything
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        # --- 2. Draw Crosshair (Green +) ---
        glColor3f(0.0, 1.0, 0.0)
        size = 15 # Size of the crosshair arms
        glLineWidth(2.0) # Make lines slightly thicker
        
        glBegin(GL_LINES)
        # Horizontal Line
        glVertex2f(cx - size, cy)
        glVertex2f(cx + size, cy)
        # Vertical Line
        glVertex2f(cx, cy - size)
        glVertex2f(cx, cy + size)
        glEnd()
        
        glLineWidth(1.0) # Reset line width

        # --- 3. Draw Text ---
        self.draw_text_gl(10, height - 40, f"Score: {score}")
        self.draw_text_gl(10, height - 80, f"Lives: {lives}")

        # --- 4. Restore 3D Mode ---
        glDisable(GL_BLEND)
        glEnable(GL_DEPTH_TEST)
        
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
        glPopMatrix()