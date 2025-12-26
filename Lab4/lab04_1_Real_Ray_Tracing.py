import sys
import math
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

# Window size
WIDTH, HEIGHT = 800, 600


def init_pygame():
    pygame.init()
    pygame.display.set_mode((WIDTH, HEIGHT), DOUBLEBUF | OPENGL)
    pygame.display.set_caption("POV-Ray Scene in PyOpenGL")


def init_opengl():
    # Background color = rgb <0.25, 0.25, 0.25>
    glClearColor(0.25, 0.25, 0.25, 1.0)

    glEnable(GL_DEPTH_TEST)
    glEnable(GL_CULL_FACE)
    glCullFace(GL_BACK)

    # Lighting
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHT1)

    # Light 0: white, translate <-5, 5, -5>
    light0_pos = [-5.0, 5.0, -5.0, 1.0]
    light0_col = [1.0, 1.0, 1.0, 1.0]
    glLightfv(GL_LIGHT0, GL_POSITION, light0_pos)
    glLightfv(GL_LIGHT0, GL_DIFFUSE,  light0_col)
    glLightfv(GL_LIGHT0, GL_SPECULAR, light0_col)

    # Light 1: rgb <0.25, 0.25, 0.25>, translate <6, -6, -6>
    light1_pos = [6.0, -6.0, -6.0, 1.0]
    light1_col = [0.25, 0.25, 0.25, 1.0]
    glLightfv(GL_LIGHT1, GL_POSITION, light1_pos)
    glLightfv(GL_LIGHT1, GL_DIFFUSE,  light1_col)
    glLightfv(GL_LIGHT1, GL_SPECULAR, light1_col)

    # Material: red with specular 0.6 (similar to POV-Ray)
    red_diffuse = [1.0, 0.0, 0.0, 1.0]
    specular = [0.6, 0.6, 0.6, 1.0]

    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, red_diffuse)
    glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, specular)
    glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, 50.0)

    # Projection (approximate POV-Ray FOV)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60.0, WIDTH / float(HEIGHT), 0.1, 100.0)

    # Modelview (camera)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    # POV-Ray: camera location <0, 0.5, -4>, look_at <0, 0, 0>
    eye = (0.0, 0.5, -4.0)
    center = (0.0, 0.0,  0.0)
    up = (0.0, 1.0, 0.0)
    gluLookAt(eye[0], eye[1], eye[2],
              center[0], center[1], center[2],
              up[0], up[1], up[2])


def draw_box():
    """
    Draw a box from <-0.5,-0.5,-0.5> to <0.5,0.5,0.5>
    with per-face normals for lighting.
    """
    # 8 vertices
    v = [
        [-0.5, -0.5, -0.5],
        [ 0.5, -0.5, -0.5],
        [ 0.5,  0.5, -0.5],
        [-0.5,  0.5, -0.5],
        [-0.5, -0.5,  0.5],
        [ 0.5, -0.5,  0.5],
        [ 0.5,  0.5,  0.5],
        [-0.5,  0.5,  0.5],
    ]

    # faces as (normal, indices)
    faces = [
        # front (z+)
        ([0.0, 0.0, 1.0],  [4, 5, 6, 7]),
        # back (z-)
        ([0.0, 0.0, -1.0], [1, 0, 3, 2]),
        # left (x-)
        ([-1.0, 0.0, 0.0], [0, 4, 7, 3]),
        # right (x+)
        ([1.0, 0.0, 0.0],  [5, 1, 2, 6]),
        # bottom (y-)
        ([0.0, -1.0, 0.0], [0, 1, 5, 4]),
        # top (y+)
        ([0.0, 1.0, 0.0],  [3, 7, 6, 2]),
    ]

    glBegin(GL_QUADS)
    for normal, idx in faces:
        glNormal3fv(normal)
        for i in idx:
            glVertex3fv(v[i])
    glEnd()


def main():
    init_pygame()
    init_opengl()

    clock = pygame.time.Clock()

    # Static POV-Ray rotation: <45,46,47> degrees
    base_rot = (45.0, 46.0, 47.0)
    # You can also animate around this base if you want:
    animate = True

    angle = 0.0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                running = False

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glPushMatrix()

        # Apply rotation similar to POV-Ray "rotate <45,46,47>"
        glRotatef(base_rot[0], 1.0, 0.0, 0.0)
        glRotatef(base_rot[1], 0.0, 1.0, 0.0)
        glRotatef(base_rot[2], 0.0, 0.0, 1.0)

        # Optional extra animation (small spin)
        if animate:
            angle += 0.5
            glRotatef(angle, 0.0, 1.0, 0.0)

        draw_box()

        glPopMatrix()

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
