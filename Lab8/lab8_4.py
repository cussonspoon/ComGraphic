import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

def load_obj(filename):
    """
    Parses a simple Wavefront .obj file.
    Supports:
     - v (vertices)
     - f (faces - triangles and quads)
    """
    vertices = []
    faces = []

    try:
        with open(filename, 'r') as f:
            for line in f:
                if line.startswith('#'): continue
                values = line.split()
                if not values: continue

                if values[0] == 'v':
                    v = list(map(float, values[1:4]))
                    vertices.append(v)

                elif values[0] == 'f':
                    face_indices = []
                    for v in values[1:]:
                        w = v.split('/')
                        face_indices.append(int(w[0]) - 1)
                    
                    if len(face_indices) == 4:
                        faces.append([face_indices[0], face_indices[1], face_indices[2]])
                        faces.append([face_indices[0], face_indices[2], face_indices[3]])
                    else:
                        faces.append(face_indices)
                        
    except IOError:
        print(f"Error: Could not open {filename}. Make sure it is in the same folder.")
        return [], []

    return vertices, faces

def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Lab 8.4 - OBJ Model Viewer")

    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0) 
    glTranslatef(0.0, 0.0, -5) 

    glEnable(GL_DEPTH_TEST)

    vertices, faces = load_obj("model.obj")
    
    angle_y = 0
    zoom = -5.0

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: 
                    pygame.quit()
                    return
                if event.key == pygame.K_r: 
                    angle_y = 0
                    zoom = -5.0

            if event.type == pygame.MOUSEWHEEL:
                zoom += event.y * 0.5 

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        angle_y += 1 

        glPushMatrix()
        
        glLoadIdentity() 
        gluPerspective(45, (display[0] / display[1]), 0.1, 50.0) 
        glTranslatef(0.0, 0.0, zoom) 
        glRotatef(angle_y, 0, 1, 0) 

        glColor3f(0.0, 1.0, 1.0) # Cyan color for the model
        glBegin(GL_TRIANGLES) 
        for face in faces:
            shade = 0.5 + (faces.index(face) % 5) * 0.1
            glColor3f(0.0, shade, shade) 

            for vertex_index in face:
                vertex = vertices[vertex_index]
                glVertex3fv(vertex)
        glEnd()
        
        glColor3f(0.0, 0.0, 0.0)
        glLineWidth(1)
        glBegin(GL_LINES)
        for face in faces:
            for i in range(len(face)):
                glVertex3fv(vertices[face[i]])
                glVertex3fv(vertices[face[(i + 1) % len(face)]])
        glEnd()

        glPopMatrix()

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()