import random
from objects.spaceship import WireframeShip
from objects.scenery import Star
from objects.asteroid import Asteroid
from objects.bullet import Bullet
from objects.powerup import PowerUp
from objects.missiles import Missile

class Level:
    def __init__(self):
        # 1. Instantiate the Ship
        self.ship = WireframeShip()
        
        # 2. Lists for Game Objects
        self.bullets = []
        self.asteroids = []
        self.stars = []
        self.powerups = []
        self.missiles = []
        
        # 3. Spawn Initial Environment
        self.spawn_objects()

    def spawn_objects(self):
        # Object Type A: Asteroids (Enemies)
        # Spawn 5, spaced far apart
        for i in range(5):
            start_pos = -50.0 - (i * 60.0)
            self.asteroids.append(Asteroid(start_z=start_pos))
            
        # Object Type B: Stars (Scenery)
        for i in range(50):
            self.stars.append(Star())
            
        # Object Type C: PowerUps (Health/Score)
        self.powerups.append(PowerUp())

    def spawn_bullet(self):
        """Fires a standard bullet from the ship's nose."""
        color = self.ship.get_current_color()
        
        # Calculate Visual Spawning Point (The Nose)
        spawn_x = self.ship.x
        spawn_y = self.ship.y - 0.5
        spawn_z = -2.3
        
        new_bullet = Bullet(spawn_x, spawn_y, spawn_z, color)
        self.bullets.append(new_bullet)

    def activate_skill(self):
        """Fires 5 Homing Missiles (The Special Skill)."""
        # 1. Check Cooldown
        if self.ship.skill_timer > 0:
            return # Skill is charging
            
        print("HOMING MISSILES FIRED!")
        # Reset Cooldown (600 frames = 10 seconds approx)
        self.ship.skill_timer = self.ship.skill_cooldown_max
        
        # 2. Define Colors for the 5 missiles
        colors = [
            (1,0,0,1), (0,1,0,1), (0,0,1,1), (1,1,0,1), (0,1,1,1)
        ]
        
        # 3. Spawn 5 Missiles
        for i in range(5):
            # Pick a random target if available
            target = None
            if len(self.asteroids) > 0:
                target = random.choice(self.asteroids)
            
            # Spawn at ship position
            new_missile = Missile(
                self.ship.x, 
                self.ship.y, 
                self.ship.z, 
                target, 
                colors[i]
            )
            self.missiles.append(new_missile)

    def update(self, mouse_dx, mouse_dy):
        # 1. Update Ship
        self.ship.update(mouse_dx, mouse_dy)
        
        # 2. Update All Lists
        for a in self.asteroids: a.update()
        for s in self.stars: s.update()
        for p in self.powerups: p.update()
        
        for b in self.bullets: b.update()
        self.bullets = [b for b in self.bullets if b.alive]
        
        for m in self.missiles: m.update()
        self.missiles = [m for m in self.missiles if m.alive]

    def draw(self):
        # Draw Scenery First
        for s in self.stars: s.draw()
        
        # Draw Objects
        for a in self.asteroids: a.draw()
        for p in self.powerups: p.draw()
        for m in self.missiles: m.draw()
        for b in self.bullets: b.draw()
        
        # Draw Ship Last (Cockpit view)
        self.ship.draw()