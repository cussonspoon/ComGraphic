import random
from objects.spaceship import WireframeShip
from objects.scenery import Star
from objects.asteroid import Asteroid
from objects.bullet import Bullet
from objects.powerup import PowerUp
from objects.missiles import Missile
from objects.pylon import ShieldPylon # <--- NEW IMPORT

class Level:
    def __init__(self):
        self.ship = WireframeShip()
        self.bullets = []
        self.asteroids = []
        self.stars = []
        self.powerups = []
        self.missiles = []
        
        # The Non-Movable Object
        self.pylon = ShieldPylon() # <--- NEW OBJECT
        
        self.spawn_objects()

    def spawn_objects(self):
        # 1. Asteroids
        for i in range(5):
            start_pos = -50.0 - (i * 60.0)
            self.asteroids.append(Asteroid(start_z=start_pos))
        # 2. Stars
        for i in range(50):
            self.stars.append(Star())
        # 3. PowerUps
        self.powerups.append(PowerUp())

    # ... (Keep spawn_bullet and activate_skill same as before) ...
    def spawn_bullet(self):
        color = self.ship.get_current_color()
        self.bullets.append(Bullet(self.ship.x, self.ship.y - 0.5, -2.3, color))

    def activate_skill(self):
        if self.ship.skill_timer > 0: return 
        self.ship.skill_timer = self.ship.skill_cooldown_max
        colors = [(1,0,0,1), (0,1,0,1), (0,0,1,1), (1,1,0,1), (0,1,1,1)]
        targets = []
        for a in self.asteroids:
            dist = (a.x - self.ship.x)**2 + (a.y - self.ship.y)**2 + (a.z - self.ship.z)**2
            targets.append((dist, a))
        targets.sort(key=lambda x: x[0])
        sorted_asteroids = [t[1] for t in targets]
        for i in range(5):
            target = None
            if len(sorted_asteroids) > 0: target = sorted_asteroids[i % len(sorted_asteroids)]
            self.missiles.append(Missile(self.ship.x, self.ship.y, self.ship.z, target, colors[i]))
    # ----------------------------------------------------------------

    def update(self, mouse_dx, mouse_dy):
        self.ship.update(mouse_dx, mouse_dy)
        self.pylon.update() # Updates timer/animation
        
        for a in self.asteroids: a.update()
        for s in self.stars: s.update()
        for p in self.powerups: p.update()
        for m in self.missiles: m.update()
        self.missiles = [m for m in self.missiles if m.alive]
        
        # --- BULLET LOGIC ---
        for b in self.bullets:
            b.update()
            if not b.alive: continue
            
            # 1. Check Collision with PYLON first
            p_dist = ((b.x - self.pylon.x)**2 + (b.y - self.pylon.y)**2 + (b.z - self.pylon.z)**2)**0.5
            if p_dist < self.pylon.radius:
                b.alive = False # Bullet hits pylon
                self.pylon.hit() # Damage pylon
                continue # Skip asteroid check for this bullet

            # 2. Check Collision with ASTEROIDS
            for a in self.asteroids:
                # Radius collision
                # Simple Sphere check
                hit = ((b.x - a.x)**2 + (b.y - a.y)**2 + (b.z - a.z)**2)**0.5 < (b.radius + 2.0)
                
                if hit:
                    b.alive = False # Bullet always dies on impact
                    
                    if self.pylon.active:
                        # SHIELDED!
                        print("SHIELD ACTIVE! Cannot destroy asteroid!")
                        # Asteroid survives
                    else:
                        # NORMAL LOGIC
                        # Check Colors (or Rainbow)
                        is_rainbow = (len(b.color) > 3 and b.color[3] == 1)
                        if is_rainbow or b.color[:3] == a.color[:3]:
                            a.reset() # Destroy Asteroid
                        else:
                            print("WRONG COLOR")
                    break

        self.bullets = [b for b in self.bullets if b.alive]

    def draw(self):
        # Draw Pylon First (Background)
        self.pylon.draw()
        
        for s in self.stars: s.draw()
        
        # Draw Asteroids
        # (We pass the 'pylon.active' state to change their color if needed)
        # Note: Since we didn't update Asteroid.draw to take arguments, 
        # we can just draw them normally, but maybe overlay a shield effect?
        # Or simply rely on the Pylon glowing to tell the player.
        for a in self.asteroids: 
            a.draw(is_invincible=self.pylon.active)
        
        for p in self.powerups: p.draw()
        for m in self.missiles: m.draw()
        for b in self.bullets: b.draw()
        self.ship.draw()