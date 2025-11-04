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