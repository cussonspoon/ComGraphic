import time
from .collision import check_sphere_collision

class GameManager:
    def __init__(self):
        self.score = 0
        self.lives = 3
        self.is_game_over = False
        
        self.ship_radius = 0.8
        self.asteroid_radius = 1.0 # Slightly larger for easier hitting
        
        self.last_hit_time = 0
        self.invulnerable_duration = 2.0

    # NOTE: Added 'bullets' parameter
    def update(self, ship, asteroids, bullets):
        if self.is_game_over:
            return

        # 1. Check: Bullet vs Asteroid
        for bullet in bullets:
            if not bullet.alive: continue
            
            for asteroid in asteroids:
                # Check collision (bullet radius is small ~0.2)
                hit = check_sphere_collision(bullet, asteroid, bullet.radius + self.asteroid_radius)
                
                if hit:
                    bullet.alive = False # Destroy bullet
                    asteroid.reset()     # Respawn asteroid
                    self.score += 10     # Bonus points
                    break                # Bullet can only hit one asteroid

        # 2. Check: Ship vs Asteroid (Your existing logic)
        if time.time() - self.last_hit_time > self.invulnerable_duration:
            for asteroid in asteroids:
                hit = check_sphere_collision(ship, asteroid, self.ship_radius + self.asteroid_radius)
                if hit:
                    self.lives -= 1
                    self.last_hit_time = time.time()
                    asteroid.reset()
                    if self.lives <= 0:
                        self.is_game_over = True
                    break

        if not self.is_game_over:
            self.score += 1 # Survival points