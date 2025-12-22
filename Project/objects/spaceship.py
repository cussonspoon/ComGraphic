from OpenGL.GL import *
import math

class WireframeShip:
    def __init__(self):
        # ... (Your existing vertices/edges code remains here) ...
        self.vertices = [
            (0.0, 0.0, -2.0), (-0.5, 0.0, 0.0), (0.5, 0.0, 0.0), (0.0, 0.5, 0.0),
            (-1.5, -0.2, 1.0), (1.5, -0.2, 1.0), (0.0, -0.2, 1.0), (0.0, 0.5, 1.0),
        ]
        self.edges = [
            (0,1), (0,2), (0,3), (1,3), (2,3), (1,2),
            (1,4), (4,6), (6,1), (2,5), (5,6), (6,2),
            (3,7), (6,7), (4,5)
        ]
        
        self.x = 0.0
        self.y = 0.0
        self.z = -5.0
        self.bank_angle = 0.0
        self.sensitivity = 0.01
        
        # --- NEW COLOR LOGIC ---
        # Default to Red active (True, False, False) or White (All False)
        # Let's start with White (All False = default safety color)
        self.red_on = False
        self.green_on = False
        self.blue_on = False

    def get_current_color(self):
        """Returns (r,g,b) based on active toggles."""
        r = 1.0 if self.red_on else 0.0
        g = 1.0 if self.green_on else 0.0
        b = 1.0 if self.blue_on else 0.0
        
        # If everything is OFF, make it White so we can see bullets
        if r == 0 and g == 0 and b == 0:
            return (1.0, 1.0, 1.0)
            
        return (r, g, b)

    def update(self, mouse_dx, mouse_dy):
        # ... (Your existing movement code remains here) ...
        self.x += mouse_dx * self.sensitivity
        self.y -= mouse_dy * self.sensitivity
        self.x = max(-4.0, min(4.0, self.x))
        self.y = max(-3.0, min(3.0, self.y))
        self.bank_angle = self.x / 4.0 

    def draw(self):
        glPushMatrix()
        glTranslatef(self.x, self.y, -5.0) 
        glRotatef(-self.bank_angle * 30.0, 0, 0, 1)
        
        glBegin(GL_LINES)
        
        # OPTIONAL: The ship itself can change color to match!
        # If you want the ship to stay Cyan, keep glColor3f(0, 1, 1)
        # If you want the ship to change color too, use this:
        current_color = self.get_current_color()
        glColor3f(current_color[0], current_color[1], current_color[2])
        
        for e in self.edges:
            for v in e:
                glVertex3fv(self.vertices[v])
        glEnd()
        glPopMatrix()