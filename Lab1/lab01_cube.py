import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

# ==============================
# 1. Define Cube Geometry

# ==============================
# TODO 1:
# Define 8 vertices of a 1x1x1 cube centered at the origin.
# - Each vertex is a tuple (x, y, z)
# - Coordinates should be combinations of -0.5 and +0.5
# - Indices must be 0..7 (8 vertices), for example:
# 0: (-0.5, -0.5, -0.5)
# ...
vertices = [
(-0.5, -0.5, -0.5),#back
(0.5, -0.5, -0.5),#back
(-0.5, 0.5, -0.5),#back
(-0.5, -0.5, 0.5),#front
(-0.5, 0.5, 0.5), #front
(0.5, -0.5, 0.5), #front
(0.5, 0.5, -0.5), #back
(0.5, 0.5, 0.5)   #front
]

# TODO 2:
# Define 12 edges as pairs of vertex indices (i, j).
# Use the SAME indexing as your vertices above.
# You need:
# - 4 edges for the back face
# - 4 edges for the front face
# - 4 edges connecting front and back faces
edges = [
(3, 4), (3, 5), (5, 7), (4, 7), (0, 1), (0, 2), (1, 6), (2, 6), (3, 0), (5, 1), (4, 2), (7, 6)
]

# ==============================
# 2. Draw Function
# ==============================
def draw_cube():
    """Draw a wireframe cube using GL_LINES."""
    glBegin(GL_LINES)
    # TODO: loop over edges and send 2 vertices per edge
    for e in edges:
        glVertex3fv(vertices[e[0]])
        glVertex3fv(vertices[e[1]])
    glEnd()
# ==============================
# 3. Main Program
# ==============================
def main():
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    # Background color (dark gray)
    glClearColor(0.1, 0.1, 0.1, 1.0)
    # Enable depth test
    glEnable(GL_DEPTH_TEST)
    # --- Projection matrix ---
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, display[0] / display[1], 0.1, 50.0)
    # Switch to modelview
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    angle = 0.0 # rotation angle

    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Clear buffers
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Reset modelview matrix
        glLoadIdentity()

        # Move the cube away from the camera
        glTranslatef(0.0, 0.0, -3.0)

        # Rotate around Y axis
        glRotatef(angle, 0.0, 1.0, 0.0)
        
        # Set line color to white
        glColor3f(1.0, 1.0, 1.0)

        # Draw cube (will work after students complete TODOs)
        draw_cube()
        
        pygame.display.flip()
        pygame.time.wait(10)
        angle += 1
    pygame.quit()

if __name__ == "__main__":
    main()