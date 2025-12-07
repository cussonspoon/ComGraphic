import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *


vertices = [
    # Body 0-7
    (-1.0, -0.5, -1.5), ( 1.0, -0.5, -1.5), ( 1.0, -0.5,  1.5), (-1.0, -0.5,  1.5),
    (-1.0,  0.0, -1.5), ( 1.0,  0.0, -1.5), ( 1.0,  0.0,  1.5), (-1.0,  0.0,  1.5),

    # Head 8-15
    (-0.6,  0.0, -0.6), ( 0.6,  0.0, -0.6), ( 0.6,  0.0,  0.6), (-0.6,  0.0,  0.6),
    (-0.5,  0.5, -0.5), ( 0.5,  0.5, -0.5), ( 0.5,  0.5,  0.5), (-0.5,  0.5,  0.5),

    # Gun 16-23
    (-0.1,  0.1,  0.5), ( 0.1,  0.1,  0.5), ( 0.1,  0.3,  0.5), (-0.1,  0.3,  0.5),
    (-0.1,  0.1,  2.0), ( 0.1,  0.1,  2.0), ( 0.1,  0.3,  2.0), (-0.1,  0.3,  2.0),

    # Hatch 24-31
    (-0.2, 0.5, -0.2),  ( 0.2, 0.5, -0.2),  ( 0.2, 0.5,  0.2),  (-0.2, 0.5,  0.2),
    (-0.2, 0.6, -0.2),  ( 0.2, 0.6, -0.2),  ( 0.2, 0.6,  0.2),  (-0.2, 0.6,  0.2),
    
    # Antenna 32,33
    (0.5, 0.5, -0.5),   (0.5, 1.5, -0.5)
]

edges = [
    # Body
    (0,1), (1,2), (2,3), (3,0), (4,5), (5,6), (6,7), (7,4), (0,4), (1,5), (2,6), (3,7),
    # Turret
    (8,9), (9,10), (10,11), (11,8), (12,13), (13,14), (14,15), (15,12), (8,12), (9,13), (10,14), (11,15),
    # Gun
    (16,17), (17,18), (18,19), (19,16), (20,21), (21,22), (22,23), (23,20), (16,20), (17,21), (18,22), (19,23),
    # Hatch
    (24,25), (25,26), (26,27), (27,24), (28,29), (29,30), (30,31), (31,28), (24,28), (25,29), (26,30), (27,31),
    # Antenna
    (32,33)
]


def draw_tank():
    glBegin(GL_LINES)
    glColor3f(0.0, 1.0, 0.0)  # Solid Green
    for e in edges:
        for vertex in e:
            glVertex3fv(vertices[vertex])
    glEnd()

def main():
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    glClearColor(0.1, 0.1, 0.1, 1.0)
    glEnable(GL_DEPTH_TEST)
    
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, display[0] / display[1], 0.1, 50.0)
    
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    
    angle = 0.0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        glTranslatef(0.0, -0.5, -7.0)
    
        glRotatef(angle, 0.0, 1.0, 0.0)
        
        draw_tank()
        
        pygame.display.flip()
        pygame.time.wait(10)
        angle += 1
        
    pygame.quit()

if __name__ == "__main__":
    main()