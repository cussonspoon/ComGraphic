from OpenGL.GL import *

def draw_colorful_cube():
    # Task 6.1: Object Geometry (Size 2 units, centered at 0,0,0)
    
    glBegin(GL_QUADS)
    
    # FRONT FACE (Red) - Normal points +Z (0, 0, 1)
    glColor3f(1.0, 0.0, 0.0) 
    glNormal3f(0.0, 0.0, 1.0) # Task 6.2: Explicit Normal
    glVertex3f(-1.0, -1.0,  1.0)
    glVertex3f( 1.0, -1.0,  1.0)
    glVertex3f( 1.0,  1.0,  1.0)
    glVertex3f(-1.0,  1.0,  1.0)

    # BACK FACE (Green) - Normal points -Z (0, 0, -1)
    glColor3f(0.0, 1.0, 0.0)
    glNormal3f(0.0, 0.0, -1.0) 
    glVertex3f(-1.0, -1.0, -1.0)
    glVertex3f(-1.0,  1.0, -1.0)
    glVertex3f( 1.0,  1.0, -1.0)
    glVertex3f( 1.0, -1.0, -1.0)

    # LEFT FACE (Blue) - Normal points -X (-1, 0, 0)
    glColor3f(0.0, 0.0, 1.0)
    glNormal3f(-1.0, 0.0, 0.0) 
    glVertex3f(-1.0, -1.0, -1.0)
    glVertex3f(-1.0, -1.0,  1.0)
    glVertex3f(-1.0,  1.0,  1.0)
    glVertex3f(-1.0,  1.0, -1.0)

    # RIGHT FACE (Yellow) - Normal points +X (1, 0, 0)
    glColor3f(1.0, 1.0, 0.0)
    glNormal3f(1.0, 0.0, 0.0) 
    glVertex3f( 1.0, -1.0, -1.0)
    glVertex3f( 1.0,  1.0, -1.0)
    glVertex3f( 1.0,  1.0,  1.0)
    glVertex3f( 1.0, -1.0,  1.0)

    # TOP FACE (Cyan) - Normal points +Y (0, 1, 0)
    glColor3f(0.0, 1.0, 1.0)
    glNormal3f(0.0, 1.0, 0.0) 
    glVertex3f(-1.0,  1.0, -1.0)
    glVertex3f(-1.0,  1.0,  1.0)
    glVertex3f( 1.0,  1.0,  1.0)
    glVertex3f( 1.0,  1.0, -1.0)

    # BOTTOM FACE (Magenta) - Normal points -Y (0, -1, 0)
    glColor3f(1.0, 0.0, 1.0)
    glNormal3f(0.0, -1.0, 0.0) 
    glVertex3f(-1.0, -1.0, -1.0)
    glVertex3f( 1.0, -1.0, -1.0)
    glVertex3f( 1.0, -1.0,  1.0)
    glVertex3f(-1.0, -1.0,  1.0)

    glEnd()