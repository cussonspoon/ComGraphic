from objects.spaceship import WireframeShip
from objects.scenery import FloorGrid
from objects.asteroid import Asteroid
from objects.bullet import Bullet

class Level:
    def __init__(self):
        # Instantiate all objects here
        self.ship = WireframeShip()
        self.floor = FloorGrid()
        self.bullets = []
        self.asteroids = []
        
        # Spawn initial asteroids
        self.spawn_asteroids()

    def spawn_asteroids(self):
        # Create 5 asteroids with large spacing
        for i in range(5):
            start_pos = -50.0 - (i * 60.0)
            self.asteroids.append(Asteroid(start_z=start_pos))

    def spawn_bullet(self):
        # Helper to create a bullet from the ship's position
        color = self.ship.get_current_color()
        new_bullet = Bullet(self.ship.x, self.ship.y, self.ship.z, color)
        self.bullets.append(new_bullet)

    def update(self, mouse_dx, mouse_dy):
        # Update Ship
        self.ship.update(mouse_dx, mouse_dy)
        
        # Update Scenery
        self.floor.update()
        
        # Update Asteroids
        for a in self.asteroids:
            a.update()

        # Update Bullets & Cleanup
        for b in self.bullets:
            b.update()
        
        # Remove dead bullets (Python list comprehension makes this clean)
        self.bullets = [b for b in self.bullets if b.alive]

    def draw(self):
        # Draw everything in the correct order
        self.floor.draw()
        
        for a in self.asteroids:
            a.draw()
            
        for b in self.bullets:
            b.draw()
            
        self.ship.draw()