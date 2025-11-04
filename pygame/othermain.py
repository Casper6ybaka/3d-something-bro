import pygame
import math

win = pygame.display.set_mode((500, 500))

width, height = 50, 50
dwin = pygame.Surface((width, height))

clock = pygame.time.Clock()

CFPS = clock.get_fps()

display_buffer = [[0, 0, 0] for _ in range(width*height)]
display_data = bytearray(color for (r, g, b) in display_buffer for color in (r, g, b))

def clearDisplay(color=(0, 0, 0)):
    global display_data
    r, g, b = color
    display_buffer = [[r, g, b] for _ in range(width*height)]
    display_data = bytearray(color for (r, g, b) in display_buffer for color in (r, g, b))

triangle = [(10, 10),
            (40, 20),
            (20, 40)]
triangle2 = [(10, 10),
            (20, 40),
            (5, 45)]

# Colors
NAVY = (0, int(0.1*255), int(0.2*255))
AQUA = (int(0.3*255), 255, int(1.0*255))
SUNFLOWER = (255, 255, int(0.6*255))
SWEETPEA = (255, int(0.7*255), int(0.75*255))
TURQUOISE = (0, 255, int(0.7*255))

def clamp(v, vmin, vmax):
    return max(vmin, min(vmax, v))

def mix(c1, c2, t):
    return [int(c1[i] * (1-t) + c2[i] * t) for i in range(3)]

def step(edge, x):
    return 1.0 if x >= edge else 0.0

def smoothstep(edge0, edge1, x):
    t = clamp((x - edge0) / (edge1 - edge0), 0.0, 1.0)
    return t * t * (3 - 2 * t)

def easeInOutCubic(t):
    t = t * 2
    if t < 1:
        return 0.5 * t * t * t
    else:
        t -= 2
        return 0.5 * (t * t * t + 2)

def linearstep(begin, end, t):
    return clamp((t - begin)/(end - begin), 0.0, 1.0)

def circle(p, radius):
    return math.sqrt(p[0]*p[0] + p[1]*p[1]) - radius

def circlePlot(p, radius):
    return 1.0 - smoothstep(0.0, 1.0/width, circle(p, radius))

def clockWipe(p, t):
    a = math.atan2(-p[0], -p[1])
    return 1.0 if t*2*math.pi > a + math.pi else 0.0

def shader(time=0):
    for x in range(width):
        for y in range(height):
            i = (x + y*width) * 3 # B B B / R G B
            pixelcolor = display_data[i:i+3]

            r = int(max(0, min(255, pixelcolor[0]+x/width*255)))
            g = int(max(0, min(255, pixelcolor[1]+y/height*255)))
            b = int(max(0, min(255, pixelcolor[2]+255)))

            display_data[i:i+3] = [r, g, b]
deltatime = clock.tick()
t = 0
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    clearDisplay()
    shader(t)
            
    dwin.blit(pygame.image.frombuffer(display_data, (width, height), "RGB"), (0, 0))
    win.blit(pygame.transform.scale(dwin, win.get_size()), (0, 0))
    
    pygame.display.update()
    deltatime = clock.tick()
    CFPS = clock.get_fps()
    pygame.display.set_caption(f"FPS: {CFPS:.1f}")
    t += deltatime