import time
from .collision import check_sphere_collision

class GameManager:
    def __init__(self):
        self.score = 0
        self.lives = 3
        self.is_game_over = False
        
        self.ship_radius = 0.8
        self.asteroid_radius = 1.0 
        
        self.last_hit_time = 0
        self.invulnerable_duration = 2.0 

    # 1. UPDATE THIS LINE: Add 'powerups' to the arguments
    def update(self, ship, asteroids, bullets, powerups):
        if self.is_game_over:
            return

        # --- A. Bullet vs Asteroid (Your existing code) ---
        for bullet in bullets:
            if not bullet.alive: continue
            
            for asteroid in asteroids:
                hit = check_sphere_collision(bullet, asteroid, bullet.radius + self.asteroid_radius)
                
                if hit:
                    if bullet.color == asteroid.color:
                        bullet.alive = False
                        asteroid.reset()
                        self.score += 10
                        print(f"MATCH! Score: {self.score}")
                    else:
                        bullet.alive = False
                        print("WRONG COLOR!")
                    break 

        # --- B. Ship vs Asteroid (Your existing code) ---
        if time.time() - self.last_hit_time > self.invulnerable_duration:
            for asteroid in asteroids:
                hit = check_sphere_collision(ship, asteroid, self.ship_radius + self.asteroid_radius)
                
                if hit:
                    self.lives -= 1
                    self.last_hit_time = time.time()
                    print(f"CRASH! Lives left: {self.lives}")
                    asteroid.reset()
                    
                    if self.lives <= 0:
                        self.is_game_over = True
                        print("GAME OVER")
                    break
        
        # --- C. NEW CODE: Ship vs PowerUp ---
        for powerup in powerups:
            if powerup.alive:
                # Check collision (Ship Radius 0.8 + PowerUp Radius 0.5)
                hit = check_sphere_collision(ship, powerup, self.ship_radius + powerup.radius)
                
                if hit:
                    self.lives += 1       # Give a life
                    self.score += 50      # Give points
                    print(f"POWERUP ACQUIRED! Lives: {self.lives}")
                    powerup.reset()       # Reset the powerup so it disappears