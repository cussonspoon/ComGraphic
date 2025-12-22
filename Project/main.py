import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

from logic.game_manager import GameManager
from logic.input import InputHandler
from logic.level import Level          
from ui.interface import Interface

def main():
    # 1. INIT
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    
    pygame.mouse.set_visible(False)
    pygame.event.set_grab(True)
    
    # Camera
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, (display[0]/display[1]), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    
    glClearColor(0.1, 0.1, 0.1, 1.0)
    glEnable(GL_DEPTH_TEST)
    
    # 2. SETUP MANAGERS
    # The Level creates and holds all the objects (ship, asteroids, etc)
    level = Level()
    game_manager = GameManager()
    input_handler = InputHandler()
    ui = Interface()
    
    clock = pygame.time.Clock()
    running = True

    # 3. GAME LOOP
    while running:
        # --- A. INPUT ---
        # Input handler modifies the 'level' (moving ship, spawning bullets)
        running = input_handler.process_input(level, game_manager)

        # --- B. LOGIC & PHYSICS ---
        if not game_manager.is_game_over:
            # The game manager checks rules using the objects inside 'level'
            game_manager.update(level.ship, level.asteroids, level.bullets)

        # --- C. DRAWING ---
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        
        # Draw the 3D world (The level handles the order)
        level.draw()
            
        # Draw the 2D UI
        ui.draw(display, game_manager.score, game_manager.lives)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()