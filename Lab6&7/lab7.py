import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math

# ==========================================
# 1. Vector Math Helpers
# ==========================================
def normalize(v):
    length = math.sqrt(v[0]**2 + v[1]**2 + v[2]**2)
    if length == 0: return [0, 0, 0]
    return [v[0]/length, v[1]/length, v[2]/length]

def sub(a, b):
    return [a[0]-b[0], a[1]-b[1], a[2]-b[2]]

def add(a, b):
    return [a[0]+b[0], a[1]+b[1], a[2]+b[2]]

def dot(a, b):
    return a[0]*b[0] + a[1]*b[1] + a[2]*b[2]

# ==========================================
# 2. Camera Class
# ==========================================
class Camera:
    def __init__(self, pos=(0, 0, 5.0)):
        self.pos = list(pos)
        self.yaw = -90.0
        self.pitch = 0.0
        
        self.forward = [0, 0, -1]
        self.right = [1, 0, 0]
        self.up = [0, 1, 0]
        self.world_up = [0, 1, 0]
        
        self.speed = 0.1
        self.sensitivity = 0.1
        self.update_vectors()

    def update_vectors(self):
        rad_yaw = math.radians(self.yaw)
        rad_pitch = math.radians(self.pitch)

        front = [0, 0, 0]
        front[0] = math.cos(rad_yaw) * math.cos(rad_pitch)
        front[1] = math.sin(rad_pitch)
        front[2] = math.sin(rad_yaw) * math.cos(rad_pitch)
        
        l = math.sqrt(front[0]**2 + front[1]**2 + front[2]**2)
        if l > 0:
            self.forward = [front[0]/l, front[1]/l, front[2]/l]

        cx = self.forward[1]*self.world_up[2] - self.forward[2]*self.world_up[1]
        cy = self.forward[2]*self.world_up[0] - self.forward[0]*self.world_up[2]
        cz = self.forward[0]*self.world_up[1] - self.forward[1]*self.world_up[0]
        l_right = math.sqrt(cx**2 + cy**2 + cz**2)
        if l_right > 0:
            self.right = [cx/l_right, cy/l_right, cz/l_right]

        ux = self.right[1]*self.forward[2] - self.right[2]*self.forward[1]
        uy = self.right[2]*self.forward[0] - self.right[0]*self.forward[2]
        uz = self.right[0]*self.forward[1] - self.right[1]*self.forward[0]
        l_up = math.sqrt(ux**2 + uy**2 + uz**2)
        if l_up > 0:
            self.up = [ux/l_up, uy/l_up, uz/l_up]

    def process_mouse(self, dx, dy):
        self.yaw += dx * self.sensitivity
        self.pitch -= dy * self.sensitivity
        if self.pitch > 89.0: self.pitch = 89.0
        if self.pitch < -89.0: self.pitch = -89.0
        self.update_vectors()

    def process_keyboard(self, keys):
        if keys[K_w]:
            self.pos[0] += self.forward[0] * self.speed
            self.pos[1] += self.forward[1] * self.speed
            self.pos[2] += self.forward[2] * self.speed
        if keys[K_s]:
            self.pos[0] -= self.forward[0] * self.speed
            self.pos[1] -= self.forward[1] * self.speed
            self.pos[2] -= self.forward[2] * self.speed
        if keys[K_a]:
            self.pos[0] -= self.right[0] * self.speed
            self.pos[1] -= self.right[1] * self.speed
            self.pos[2] -= self.right[2] * self.speed
        if keys[K_d]:
            self.pos[0] += self.right[0] * self.speed
            self.pos[1] += self.right[1] * self.speed
            self.pos[2] += self.right[2] * self.speed

    def apply(self):
        target = [self.pos[0] + self.forward[0],
                  self.pos[1] + self.forward[1],
                  self.pos[2] + self.forward[2]]
        gluLookAt(self.pos[0], self.pos[1], self.pos[2],
                  target[0], target[1], target[2],
                  self.up[0], self.up[1], self.up[2])

# ==========================================
# 3. Manual Lighting (Mode 1 & 2)
# ==========================================
def compute_lighting(pos, normal, light_pos, cam_pos, base_color, mode):
    l = normalize(sub(light_pos, pos))
    v = normalize(sub(cam_pos, pos))
    n = normalize(normal)

    # --- Diffuse (Task 7.1) ---
    diffuse = max(0.0, dot(n, l))
    
    # --- Specular (Task 7.2) ---
    specular = 0.0
    
    # Only calculate specular if Mode is 2 (Phong/Blinn)
    if mode == 2:
        h = normalize(add(l, v))
        if diffuse > 0:
            specular = math.pow(max(0.0, dot(n, h)), 64.0)

    # Combine
    ambient = 0.2
    
    r = (ambient + diffuse) * base_color[0] + specular
    g = (ambient + diffuse) * base_color[1] + specular
    b = (ambient + diffuse) * base_color[2] + specular

    return [min(1.0, max(0.0, r)), 
            min(1.0, max(0.0, g)), 
            min(1.0, max(0.0, b))]

# ==========================================
# 4. Draw Cube
# ==========================================
def draw_lit_cube(light_pos, cam_pos, mode):
    v = [
        [-1, -1,  1], [ 1, -1,  1], [ 1,  1,  1], [-1,  1,  1], # Front
        [-1, -1, -1], [-1,  1, -1], [ 1,  1, -1], [ 1, -1, -1], # Back
        [-1, -1, -1], [-1, -1,  1], [-1,  1,  1], [-1,  1, -1], # Left
        [ 1, -1, -1], [ 1,  1, -1], [ 1,  1,  1], [ 1, -1,  1], # Right
        [-1,  1, -1], [-1,  1,  1], [ 1,  1,  1], [ 1,  1, -1], # Top
        [-1, -1, -1], [ 1, -1, -1], [ 1, -1,  1], [-1, -1,  1]  # Bottom
    ]
    n = [[0,0,1], [0,0,-1], [-1,0,0], [1,0,0], [0,1,0], [0,-1,0]]
    colors = [[1,0,0], [0,1,0], [0,0,1], [1,1,0], [0,1,1], [1,0,1]]

    glBegin(GL_QUADS)
    for i in range(6):
        normal = n[i]
        base_c = colors[i]
        for j in range(4):
            idx = i * 4 + j
            vertex = v[idx]
            # Pass 'mode' to the lighting function
            final_color = compute_lighting(vertex, normal, light_pos, cam_pos, base_c, mode)
            glColor3fv(final_color)
            glVertex3fv(vertex)
    glEnd()

# ==========================================
# 5. Main Loop
# ==========================================
def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Lab 7 - Keys: 1=Lambert, 2=Phong | Arrows=Light")
    
    glClearColor(0.0, 0.0, 0.0, 1.0) 

    center_x, center_y = display[0] // 2, display[1] // 2
    pygame.event.set_grab(True)
    pygame.mouse.set_visible(False)
    pygame.mouse.set_pos((center_x, center_y))

    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)
    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)

    camera = Camera(pos=(0, 0, 5.0))
    light_pos = [2.0, 2.0, 4.0]
    
    # Default Shading Mode: 2 (Phong with Spot)
    shading_mode = 2 
    
    clock = pygame.time.Clock()
    running = True
    first_frame = True

    while running:
        clock.tick(60)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                if event.key == K_r: 
                    camera = Camera(pos=(0, 0, 5.0))
                    first_frame = True
                
                # --- SHADING TOGGLE ---
                if event.key == K_1:
                    shading_mode = 1 # Lambertian Only (No Spot)
                    pygame.display.set_caption("Lab 7 - Mode: Lambertian (No Spot)")
                if event.key == K_2:
                    shading_mode = 2 # Blinn-Phong (With Spot)
                    pygame.display.set_caption("Lab 7 - Mode: Blinn-Phong (With Spot)")

        keys = pygame.key.get_pressed()
        
        # Light Control
        if keys[K_LEFT]:  light_pos[0] -= 0.1
        if keys[K_RIGHT]: light_pos[0] += 0.1
        if keys[K_UP]:    light_pos[1] += 0.1
        if keys[K_DOWN]:  light_pos[1] -= 0.1
        if keys[K_PLUS] or keys[K_KP_PLUS] or keys[K_EQUALS]: 
            light_pos[2] += 0.1
        if keys[K_MINUS] or keys[K_KP_MINUS]: 
            light_pos[2] -= 0.1

        camera.process_keyboard(keys)

        # Mouse
        mx, my = pygame.mouse.get_pos()
        dx, dy = mx - center_x, my - center_y
        
        if (dx != 0 or dy != 0) and not first_frame:
            camera.process_mouse(dx, dy)
            pygame.mouse.set_pos((center_x, center_y))
        
        if first_frame:
            pygame.mouse.set_pos((center_x, center_y))
            first_frame = False

        # Render
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        
        camera.apply()
        
        # Draw Light
        glPushMatrix()
        glTranslatef(light_pos[0], light_pos[1], light_pos[2])
        glColor3f(1,1,1)
        glPointSize(10)
        glBegin(GL_POINTS)
        glVertex3f(0,0,0)
        glEnd()
        glPopMatrix()
        
        # Draw Cube (Pass shading_mode)
        draw_lit_cube(light_pos, camera.pos, shading_mode)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()