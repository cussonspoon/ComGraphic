import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

from objects.spaceship import WireframeShip
from objects.scenery import FloorGrid
from objects.asteroid import Asteroid
from objects.bullet import Bullet      # <--- New Import
from logic.game_manager import GameManager
from ui.interface import Interface

def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    
    # Hide mouse and grab input
    pygame.mouse.set_visible(False)
    pygame.event.set_grab(True)
    
    # Camera Setup
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, (display[0]/display[1]), 0.1, 100.0) # Increased view distance to 100
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    
    glClearColor(0.1, 0.1, 0.1, 1.0)
    glEnable(GL_DEPTH_TEST)
    
    # Objects
    ship = WireframeShip()
    floor = FloorGrid()
    game_manager = GameManager()
    ui = Interface()
    
    asteroids = []
    for i in range(15): # Added a few more asteroids
        asteroids.append(Asteroid())

    bullets = [] # <--- List to hold active bullets

    clock = pygame.time.Clock()
    running = True

    while running:
        # --- A. EVENTS ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                
                # SHOOTING (Spacebar)
                if event.key == pygame.K_SPACE and not game_manager.is_game_over:
                    # Create bullet at ship's current position
                    new_bullet = Bullet(ship.x, ship.y, ship.z)
                    bullets.append(new_bullet)

        # --- B. UPDATES ---
        if not game_manager.is_game_over:
            mouse_dx, mouse_dy = pygame.mouse.get_rel()
            ship.update(mouse_dx, mouse_dy)
            floor.update()
            
            for a in asteroids:
                a.update()

            # Update Bullets
            for b in bullets:
                b.update()
            
            # Remove dead bullets (performance cleanup)
            bullets = [b for b in bullets if b.alive]

            # Pass bullets to manager for collision checks
            game_manager.update(ship, asteroids, bullets)
        
        else:
            pygame.event.set_grab(False)
            pygame.mouse.set_visible(True)

        # --- C. DRAWING ---
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        
        floor.draw()
        
        for a in asteroids:
            a.draw()
            
        for b in bullets:
            b.draw()
            
        if not game_manager.is_game_over:
            ship.draw()
            
        ui.draw(display, game_manager.score, game_manager.lives)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()