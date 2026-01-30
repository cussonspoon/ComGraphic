import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math


vertices = [
    (1, -1, -1), (1, 1, -1), (-1, 1, -1), (-1, -1, -1),
    (1, -1, 1), (1, 1, 1), (-1, -1, 1), (-1, 1, 1)
]
surfaces = [
    (0,1,2,3), (3,2,7,6), (6,7,5,4),
    (4,5,1,0), (1,5,7,2), (4,0,3,6)
]
edges = [
    (0,1), (1,2), (2,3), (3,0),
    (4,5), (5,6), (6,7), (7,4),
    (0,4), (1,5), (2,6), (3,7)
]

def draw_cube_solid(color):
    """
    Renders a cube with a single solid color and black outlines.
    args:
        color: tuple (r, g, b)
    """
    glBegin(GL_QUADS)
    glColor3fv(color)
    for surface in surfaces:
        for vertex in surface:
            glVertex3fv(vertices[vertex])
    glEnd()

    glLineWidth(2)
    glBegin(GL_LINES)
    glColor3fv((0, 0, 0))
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()

def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Lab 8.3 - 3D Perspective & Depth")

    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LESS)

    glTranslatef(0.0, 0.0, -5)

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return # Clean exit

        angle = pygame.time.get_ticks() * 0.05 
        oscillation = math.sin(pygame.time.get_ticks() * 0.002) * 2.5 

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glPushMatrix()
        glTranslatef(-0.8, 0, -10) 
        glRotatef(angle, 1, 1, 0) # Continuous rotation
        draw_cube_solid((0.6, 1.0, 1.0)) # Light Cyan
        glPopMatrix()
        glPushMatrix()
        glTranslatef(oscillation, 1, -15) 
        draw_cube_solid((1.0, 0.6, 1.0)) # Light Magenta
        glPopMatrix()
        glPushMatrix()
        glTranslatef(1.5, -1, -25)
        glRotatef(-angle/2, 0, 1, 0) 
        draw_cube_solid((1.0, 1.0, 0.6)) # Light Yellow
        glPopMatrix()

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()