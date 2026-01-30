import pygame
import sys


WIDTH, HEIGHT = 800, 600
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Lab 8.1 - Bresenham Line Drawing")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

def draw_bresenham_line(surface, p0, p1, color):
    x0, y0 = p0
    x1, y1 = p1

    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy

    while True:
        surface.set_at((x0, y0), color)

        if x0 == x1 and y0 == y1:
            break

        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x0 += sx
        if e2 < dx:
            err += dx
            y0 += sy

def main():
    clock = pygame.time.Clock()
    points = []
    lines = []

    print("Left click: pick P0 then P1 | Press C to clear | Close window to exit")

    while True:
        screen.fill(BLACK)

        for line in lines:
            draw_bresenham_line(screen, line[0], line[1], WHITE)

        if len(points) == 1:
            pygame.draw.circle(screen, RED, points[0], 3)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = event.pos
                points.append(pos)
                
                if len(points) == 2:
                    print(f"P0={points[0]}, P1={points[1]}")
                    lines.append((points[0], points[1]))
                    points = []

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    lines = []

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()