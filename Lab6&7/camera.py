import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math

# Import the cube drawing function from the other file
import cube

# ==========================================
# Task 6.3: Camera Class Implementation
# ==========================================
class Camera:
    def __init__(self, pos=(0, 0, 5)):
        # Camera attributes
        self.pos = list(pos)
        self.yaw = -90.0   # Looking towards negative Z
        self.pitch = 0.0
        
        # Orientation vectors (initialized in update_vectors)
        self.forward = [0, 0, -1]
        self.right = [1, 0, 0]
        self.up = [0, 1, 0]
        self.world_up = [0, 1, 0]
        
        self.speed = 0.1
        self.sensitivity = 0.1
        
        self.update_vectors()

    def update_vectors(self):
        # Calculate new forward vector based on Yaw and Pitch
        rad_yaw = math.radians(self.yaw)
        rad_pitch = math.radians(self.pitch)

        front = [0, 0, 0]
        front[0] = math.cos(rad_yaw) * math.cos(rad_pitch)
        front[1] = math.sin(rad_pitch)
        front[2] = math.sin(rad_yaw) * math.cos(rad_pitch)

        # Normalize forward vector
        length = math.sqrt(front[0]**2 + front[1]**2 + front[2]**2)
        self.forward = [front[0]/length, front[1]/length, front[2]/length]

        # Calculate Right vector (Cross product of Forward and World Up)
        cx, cy, cz = self.cross_product(self.forward, self.world_up)
        # Normalize right
        l_right = math.sqrt(cx**2 + cy**2 + cz**2)
        self.right = [cx/l_right, cy/l_right, cz/l_right]

        # Calculate Up vector (Cross product of Right and Forward)
        ux, uy, uz = self.cross_product(self.right, self.forward)
        l_up = math.sqrt(ux**2 + uy**2 + uz**2)
        self.up = [ux/l_up, uy/l_up, uz/l_up]

    def cross_product(self, a, b):
        return (a[1]*b[2] - a[2]*b[1],
                a[2]*b[0] - a[0]*b[2],
                a[0]*b[1] - a[1]*b[0])

    def process_mouse(self, dx, dy):
        # Update angles based on mouse delta
        self.yaw += dx * self.sensitivity
        self.pitch -= dy * self.sensitivity 

        # Clamp pitch so screen doesn't flip
        if self.pitch > 89.0: self.pitch = 89.0
        if self.pitch < -89.0: self.pitch = -89.0
        
        self.update_vectors()

    def process_keyboard(self, keys):
        # W/S = Forward/Backward
        if keys[K_w]:
            self.pos[0] += self.forward[0] * self.speed
            self.pos[1] += self.forward[1] * self.speed
            self.pos[2] += self.forward[2] * self.speed
        if keys[K_s]:
            self.pos[0] -= self.forward[0] * self.speed
            self.pos[1] -= self.forward[1] * self.speed
            self.pos[2] -= self.forward[2] * self.speed
        
        # A/D = Strafe Left/Right
        if keys[K_a]:
            self.pos[0] -= self.right[0] * self.speed
            self.pos[1] -= self.right[1] * self.speed
            self.pos[2] -= self.right[2] * self.speed
        if keys[K_d]:
            self.pos[0] += self.right[0] * self.speed
            self.pos[1] += self.right[1] * self.speed
            self.pos[2] += self.right[2] * self.speed

    def apply(self):
        # Apply the view matrix using gluLookAt
        center = [self.pos[0] + self.forward[0],
                  self.pos[1] + self.forward[1],
                  self.pos[2] + self.forward[2]]
        
        gluLookAt(self.pos[0], self.pos[1], self.pos[2],
                  center[0], center[1], center[2],
                  self.up[0], self.up[1], self.up[2])

# ==========================================
# Main Loop
# ==========================================
def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Task 6: Infinite Camera")
    
    # 1. Define the center of the screen
    center_x, center_y = display[0] // 2, display[1] // 2

    # 2. Lock mouse and force it to center immediately
    pygame.event.set_grab(True)
    pygame.mouse.set_visible(False)
    pygame.mouse.set_pos((center_x, center_y))

    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)
    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)

    camera = Camera(pos=(0, 0, 5))
    clock = pygame.time.Clock()

    running = True
    while running:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False


        # A. Get current mouse position
        mx, my = pygame.mouse.get_pos()
        
        # B. Calculate how far it moved from the center
        dx = mx - center_x
        dy = my - center_y
        
        # C. Apply rotation if there was movement
        if dx != 0 or dy != 0:
            camera.process_mouse(dx, dy)
            # D. RESET mouse back to center so it never hits the edge
            pygame.mouse.set_pos((center_x, center_y))
        # ============================================

        keys = pygame.key.get_pressed()
        camera.process_keyboard(keys)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        
        camera.apply()
        cube.draw_colorful_cube()

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()