from objects.spaceship import WireframeShip
from objects.scenery import Star        # <--- UPDATED IMPORT
from objects.asteroid import Asteroid
from objects.bullet import Bullet
from objects.powerup import PowerUp

class Level:
    def __init__(self):
        self.ship = WireframeShip()
        self.bullets = []
        self.asteroids = []
        self.stars = []
        self.powerups = []
        
        self.spawn_objects()

    def spawn_objects(self):
        # 1. Asteroids
        for i in range(5):
            start_pos = -50.0 - (i * 60.0)
            self.asteroids.append(Asteroid(start_z=start_pos))
            
        # 2. Stars (Background Scenery)
        for i in range(50):
            self.stars.append(Star())
            
        # 3. PowerUps
        self.powerups.append(PowerUp())

    def spawn_bullet(self):
        # 1. Get current color
        color = self.ship.get_current_color()
        
        # 2. Calculate Visual Spawning Point (The Nose)
        # We match the offsets used in spaceship.draw()
        spawn_x = self.ship.x
        spawn_y = self.ship.y - 0.5  # Lowered to match cockpit height
        spawn_z = -2.3               # Forward to match nose tip
        
        # 3. Create Bullet
        new_bullet = Bullet(spawn_x, spawn_y, spawn_z, color)
        
        # Optional: slight upward angle so it converges on crosshair?
        # For now, shooting straight forward is usually best for this style.
        
        self.bullets.append(new_bullet)

    def update(self, mouse_dx, mouse_dy):
        self.ship.update(mouse_dx, mouse_dy)
        
        for a in self.asteroids: a.update()
        for b in self.bullets: b.update()
        self.bullets = [b for b in self.bullets if b.alive]
        
        for s in self.stars: s.update()
        for p in self.powerups: p.update()

    def draw(self):
        # Draw background stars first
        for s in self.stars: s.draw()
        
        for a in self.asteroids: a.draw()
        for p in self.powerups: p.draw()
        for b in self.bullets: b.draw()
        self.ship.draw()