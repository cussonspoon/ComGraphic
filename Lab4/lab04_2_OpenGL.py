import math
import pygame

def v_add(a, b):
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])

def v_sub(a, b):
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])

def v_mul(a, s):
    return (a[0] * s, a[1] * s, a[2] * s)

def v_div(a, s):
    return (a[0] / s, a[1] / s, a[2] / s)

def v_dot(a, b):
    return a[0]*b[0] + a[1]*b[1] + a[2]*b[2]

def v_length(a):
    return math.sqrt(v_dot(a, a))

def v_norm(a):
    l = v_length(a)
    if l == 0:
        return (0.0, 0.0, 0.0)
    return (a[0]/l, a[1]/l, a[2]/l)

def v_cross(a, b):
    return (a[1]*b[2] - a[2]*b[1],
            a[2]*b[0] - a[0]*b[2],
            a[0]*b[1] - a[1]*b[0])

def v_reflect(i, n):
    dot = v_dot(i, n)
    return v_sub(i, v_mul(n, 2.0 * dot))

def intersect_sphere(ray_origin, ray_dir):
    c = (0.0, 0.0, 0.0)
    r = 1.0

    e = ray_origin
    d = ray_dir

    oc = v_sub(e, c)

    A = v_dot(d, d)
    B = 2.0 * v_dot(oc, d)
    C = v_dot(oc, oc) - (r * r)

    discriminant = B*B - 4*A*C

    if discriminant < 0:
        return (False, None, None)

    sqrt_disc = math.sqrt(discriminant)
    t1 = (-B - sqrt_disc) / (2.0 * A)
    t2 = (-B + sqrt_disc) / (2.0 * A)

    t = float('inf')
    if t1 > 1e-4:
        t = t1
    elif t2 > 1e-4:
        t = t2

    if t == float('inf'):
        return (False, None, None)

    p = v_add(e, v_mul(d, t))
    p_minus_c = v_sub(p, c)
    n = v_div(p_minus_c, r)

    return (True, t, n)

def trace_ray(ray_origin, ray_dir, lights, background_color):
    hit, t, hit_normal = intersect_sphere(ray_origin, ray_dir)

    if not hit:
        return background_color

    p = v_add(ray_origin, v_mul(ray_dir, t))

    base_color = (1.0, 0.0, 0.0)
    spec_color = (0.6, 0.6, 0.6)
    ambient_k = 0.1
    shininess = 50.0

    r, g, b = [ambient_k * c for c in base_color]
    
    view_dir = v_norm(v_mul(ray_dir, -1.0))

    for light_pos, light_col in lights:
        L_vec = v_sub(light_pos, p)
        L = v_norm(L_vec)
        
        ndotl = v_dot(hit_normal, L)
        if ndotl > 0.0:
            diff = ndotl
            
            refl = v_reflect(v_mul(L, -1.0), hit_normal)
            rv = max(0.0, v_dot(refl, view_dir))
            
            if rv > 0.0:
                spec = rv ** shininess
            else:
                spec = 0.0

            r += light_col[0] * (base_color[0] * diff + spec_color[0] * spec)
            g += light_col[1] * (base_color[1] * diff + spec_color[1] * spec)
            b += light_col[2] * (base_color[2] * diff + spec_color[2] * spec)

    r = max(0.0, min(1.0, r))
    g = max(0.0, min(1.0, g))
    b = max(0.0, min(1.0, b))
    
    return (r, g, b)

def render(width, height):
    eye     = (0.0, 0.5, -4.0)
    look_at = (0.0, 0.0,  0.0)
    up      = (0.0, 1.0,  0.0)

    fov_y = math.radians(60.0)
    aspect = width / float(height)

    forward = v_norm(v_sub(look_at, eye))
    right   = v_norm(v_cross(forward, up))
    up_cam  = v_cross(right, forward)

    half_h = math.tan(fov_y / 2.0)
    half_w = aspect * half_h

    lights = [
        ((-5.0,  5.0, -5.0), (1.0, 1.0, 1.0)),
        (( 6.0, -6.0, -6.0), (0.25, 0.25, 0.25)),
    ]
    background_color = (0.25, 0.25, 0.25)

    framebuffer = [[(0, 0, 0) for _ in range(width)] for _ in range(height)]

    for j in range(height):
        ndc_y = 1.0 - 2.0 * (j + 0.5) / float(height)
        
        for i in range(width):
            ndc_x = 2.0 * (i + 0.5) / float(width) - 1.0

            px = ndc_x * half_w
            py = ndc_y * half_h

            dir_world = v_add(
                forward,
                v_add(v_mul(right, px), v_mul(up_cam, py))
            )
            dir_world = v_norm(dir_world)

            color = trace_ray(eye, dir_world, lights, background_color)
            
            framebuffer[j][i] = (
                int(color[0]*255),
                int(color[1]*255),
                int(color[2]*255),
            )

    return framebuffer

def main():
    width, height = 320, 240

    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("CPU Ray Tracer - Analytic Sphere")

    surface = pygame.Surface((width, height))
    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        framebuffer = render(width, height)

        for y in range(height):
            for x in range(width):
                surface.set_at((x, y), framebuffer[y][x])

        screen.blit(surface, (0, 0))
        pygame.display.flip()

        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()