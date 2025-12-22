import pygame
from OpenGL.GL import *
from OpenGL.GLU import *

class Interface:
    def __init__(self):
        pygame.font.init()
        self.font = pygame.font.SysFont("Arial", 32, bold=True)
        self.text_color = (255, 255, 255, 255)

    def draw_text_gl(self, x, y, text_string):
        """Helper to render text in OpenGL"""
        text_surface = self.font.render(text_string, True, self.text_color, (0, 0, 0, 0))
        text_data = pygame.image.tostring(text_surface, "RGBA", True)
        width, height = text_surface.get_width(), text_surface.get_height()
        glRasterPos2i(x, y)
        glDrawPixels(width, height, GL_RGBA, GL_UNSIGNED_BYTE, text_data)

    def draw(self, display_size, score, lives, skill_timer, skill_max):
        """
        Draws the 2D Overlay: Crosshair, HUD, and Skill Bar.
        """
        width, height = display_size
        cx, cy = width // 2, height // 2

        # --- Switch to 2D Orthographic Projection ---
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

        # 1. CROSSHAIR (Green +)
        glColor3f(0.0, 1.0, 0.0)
        size = 15
        glLineWidth(2.0)
        glBegin(GL_LINES)
        glVertex2f(cx - size, cy)
        glVertex2f(cx + size, cy)
        glVertex2f(cx, cy - size)
        glVertex2f(cx, cy + size)
        glEnd()
        glLineWidth(1.0)

        # 2. SKILL BAR (Bottom Center)
        bar_width = 200
        bar_height = 20
        bx = cx - (bar_width // 2)
        by = 50 # Position from bottom
        
        # Calculate Fill
        if skill_timer <= 0:
            fill_pct = 1.0
            color = (0, 1.0, 1.0) # Cyan (Ready)
            label = "SKILL READY [E]"
        else:
            fill_pct = 1.0 - (skill_timer / skill_max)
            color = (0.5, 0.5, 0.5) # Grey (Charging)
            label = "CHARGING..."

        # Draw Bar Background (Outline)
        glColor3f(1, 1, 1) # White
        glBegin(GL_LINE_LOOP)
        glVertex2f(bx, by)
        glVertex2f(bx + bar_width, by)
        glVertex2f(bx + bar_width, by + bar_height)
        glVertex2f(bx, by + bar_height)
        glEnd()

        # Draw Bar Fill
        current_w = bar_width * fill_pct
        glColor3f(color[0], color[1], color[2])
        glBegin(GL_QUADS)
        glVertex2f(bx, by)
        glVertex2f(bx + current_w, by)
        glVertex2f(bx + current_w, by + bar_height)
        glVertex2f(bx, by + bar_height)
        glEnd()
        
        # Draw Skill Label
        self.draw_text_gl(bx, by + 25, label)

        # 3. HUD TEXT (Score & Lives)
        self.draw_text_gl(10, height - 40, f"Score: {score}")
        self.draw_text_gl(10, height - 80, f"Lives: {lives}")

        # --- Restore 3D Projection ---
        glDisable(GL_BLEND)
        glEnable(GL_DEPTH_TEST)
        
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
        glPopMatrix()