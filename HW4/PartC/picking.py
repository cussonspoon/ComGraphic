import math
import pygame
from OpenGL.GL import *
from OpenGL.GLU import *

def get_ray_from_mouse(mouse_x, mouse_y):
    """
    Converts 2D mouse coordinates to a 3D ray (origin, direction).
    """
    # Get current viewport, modelview, and projection matrices
    viewport = glGetIntegerv(GL_VIEWPORT)
    modelview = glGetDoublev(GL_MODELVIEW_MATRIX)
    projection = glGetDoublev(GL_PROJECTION_MATRIX)

    # OpenGL y-coordinate is inverted relative to PyGame
    win_x = float(mouse_x)
    win_y = float(viewport[3] - mouse_y)

    # Unproject (x, y, 0.0) -> Point on near plane
    # Unproject (x, y, 1.0) -> Point on far plane
    try:
        start = gluUnProject(win_x, win_y, 0.0, modelview, projection, viewport)
        end = gluUnProject(win_x, win_y, 1.0, modelview, projection, viewport)
    except:
        return None, None

    # Ray direction is vector from start to end
    direction = [end[0] - start[0], end[1] - start[1], end[2] - start[2]]
    
    # Normalize direction
    length = math.sqrt(direction[0]**2 + direction[1]**2 + direction[2]**2)
    if length == 0: return None, None
    direction = [d / length for d in direction]

    return start, direction

def ray_sphere_intersect(ray_origin, ray_dir, sphere_center, sphere_radius):
    """
    Returns distance to intersection if hit, else None.
    Math: |(O + tD) - C|^2 = r^2
    """
    ox, oy, oz = ray_origin
    dx, dy, dz = ray_dir
    cx, cy, cz = sphere_center
    
    # Vector from Ray Origin to Sphere Center
    fx = ox - cx
    fy = oy - cy
    fz = oz - cz

    # Quadratic equation coefficients: a*t^2 + b*t + c = 0
    # a = dot(D, D) = 1 (since D is normalized)
    b = 2.0 * (fx*dx + fy*dy + fz*dz)
    c = (fx*fx + fy*fy + fz*fz) - sphere_radius*sphere_radius

    discriminant = b*b - 4.0*c

    if discriminant < 0:
        return None # No intersection

    # Calculate nearest t
    t = (-b - math.sqrt(discriminant)) / 2.0
    
    if t < 0:
        return None # Intersection is behind the camera
        
    return t