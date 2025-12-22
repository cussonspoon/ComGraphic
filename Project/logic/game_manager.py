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

    def update(self, ship, asteroids, bullets):
        if self.is_game_over:
            return

        # 1. Check: Bullet vs Asteroid
        for bullet in bullets:
            if not bullet.alive: continue
            
            for asteroid in asteroids:
                hit = check_sphere_collision(bullet, asteroid, bullet.radius + self.asteroid_radius)
                
                if hit:
                    # --- NEW COLOR CHECK ---
                    # Compare tuples directly: (1.0, 0.0, 0.0) == (1.0, 0.0, 0.0) works well in Python
                    if bullet.color == asteroid.color:
                        bullet.alive = False # Destroy bullet
                        asteroid.reset()     # Destroy asteroid
                        self.score += 10
                        print(f"MATCH! Score: {self.score}")
                    else:
                        # WRONG COLOR
                        bullet.alive = False # Bullet hits but does nothing (absorbed)
                        print("WRONG COLOR!")
                    
                    break # Bullet only hits one thing

        # 2. Check: Ship vs Asteroid (Damage Logic - No color protection here!)
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