import math

def check_sphere_collision(obj1, obj2, radius_sum):
    """
    Returns True if the distance between obj1 and obj2 is less than radius_sum.
    Both objects must have .x, .y, and .z attributes.
    """
    dx = obj1.x - obj2.x
    dy = obj1.y - obj2.y
    dz = obj1.z - obj2.z
    
    # Distance formula: sqrt(x^2 + y^2 + z^2)
    distance = math.sqrt(dx*dx + dy*dy + dz*dz)
    
    return distance < radius_sum