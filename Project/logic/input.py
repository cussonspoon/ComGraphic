import pygame

class InputHandler:
    def process_input(self, level, game_manager):
        """
        Handles input and delegates actions to the Level.
        """
        # 1. Event Loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                
                # Colors (Access ship via level)
                if event.key == pygame.K_1:
                    level.ship.red_on = not level.ship.red_on
                if event.key == pygame.K_2:
                    level.ship.green_on = not level.ship.green_on
                if event.key == pygame.K_3:
                    level.ship.blue_on = not level.ship.blue_on

                # Shooting (Use the level's helper method)
                if event.key == pygame.K_SPACE and not game_manager.is_game_over:
                    level.spawn_bullet()

                if event.key == pygame.K_e:
                    level.activate_skill()

        # 2. Continuous Input (Mouse)
        if not game_manager.is_game_over:
            mouse_dx, mouse_dy = pygame.mouse.get_rel()
            # Pass movement to level
            level.update(mouse_dx, mouse_dy)
        else:
            pygame.event.set_grab(False)
            pygame.mouse.set_visible(True)

        return True