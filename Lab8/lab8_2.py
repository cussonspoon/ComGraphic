import pygame
import sys

WIDTH, HEIGHT = 800, 600
A = (200, 120)
B = (120, 420)
C = (520, 380)
CA = (255, 0, 0)   
CB = (0, 255, 0)   
CC = (0, 0, 255)  

def get_barycentric(p, a, b, c):
    """
    Computes alpha, beta, gamma for point p relative to triangle abc[cite: 58].
    Using the edge-function method for software rasterization[cite: 77].
    """
    det = (b[1] - c[1]) * (a[0] - c[0]) + (c[0] - b[0]) * (a[1] - c[1])
    
    if abs(det) < 1e-6:
        return -1, -1, -1

    alpha = ((b[1] - c[1]) * (p[0] - c[0]) + (c[0] - b[0]) * (p[1] - c[1])) / det
    beta = ((c[1] - a[1]) * (p[0] - c[0]) + (a[0] - c[0]) * (p[1] - c[1])) / det
    gamma = 1.0 - alpha - beta
    
    return alpha, beta, gamma

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Lab 8.2 - Software Triangle Rasterization (Gouraud)")
    
    min_x = int(min(A[0], B[0], C[0]))
    max_x = int(max(A[0], B[0], C[0]))
    min_y = int(min(A[1], B[1], C[1]))
    max_y = int(max(A[1], B[1], C[1]))

    running = True
    show_wireframe = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_w:
                    show_wireframe = not show_wireframe

        screen.fill((0, 0, 0)) 

        for x in range(min_x, max_x + 1):
            for y in range(min_y, max_y + 1):
                alpha, beta, gamma = get_barycentric((x, y), A, B, C)
                
                if alpha >= 0 and beta >= 0 and gamma >= 0:
                    r = int(alpha * CA[0] + beta * CB[0] + gamma * CC[0])
                    g = int(alpha * CA[1] + beta * CB[1] + gamma * CC[1])
                    b = int(alpha * CA[2] + beta * CB[2] + gamma * CC[2])
                    
                    screen.set_at((x, y), (r, g, b))

        if show_wireframe:
            pygame.draw.line(screen, (255, 255, 255), A, B)
            pygame.draw.line(screen, (255, 255, 255), B, C)
            pygame.draw.line(screen, (255, 255, 255), C, A)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()