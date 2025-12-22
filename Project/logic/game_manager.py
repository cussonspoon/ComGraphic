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

    # 1. UPDATE THIS LINE: Add 'powerups' and 'missiles' to the arguments
    def update(self, ship, asteroids, bullets, powerups, missiles):
        if self.is_game_over:
            return

        # --- A. CHECK BULLETS (Standard) ---
        for bullet in bullets:
            if not bullet.alive: continue
            
            for asteroid in asteroids:
                if check_sphere_collision(bullet, asteroid, bullet.radius + self.asteroid_radius):
                    # Check the 4th value (Flag)
                    # bullet.color[3] is the flag. 
                    # Standard bullets are (r,g,b,0), so this is False.
                    is_rainbow = (len(bullet.color) > 3 and bullet.color[3] == 1)
                    
                    # Logic: If Rainbow OR Colors Match -> Destroy
                    if is_rainbow or bullet.color[:3] == asteroid.color[:3]:
                        bullet.alive = False
                        asteroid.reset()
                        self.score += 10
                    else:
                        bullet.alive = False # Wrong color, just destroy bullet
                    break

        # --- B. CHECK MISSILES (Special) ---
        for m in missiles:
            if not m.alive: continue
            
            for a in asteroids:
                if check_sphere_collision(m, a, m.radius + self.asteroid_radius):
                    # Missiles are spawned with (r,g,b,1), so they ALWAYS hit.
                    # We can technically skip the check, but using the flag makes it robust.
                    is_rainbow = (len(m.color) > 3 and m.color[3] == 1)
                    
                    if is_rainbow:
                        m.alive = False
                        a.reset()
                        self.score += 20
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