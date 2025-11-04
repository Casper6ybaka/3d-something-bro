import pygame

win = pygame.display.set_mode((500, 500))

width, height = 50, 50
dwin = pygame.Surface((width, height))

clock = pygame.time.Clock()

CFPS = clock.get_fps()

display_buffer = [[0, 0, 0] for _ in range(width*height)]

triangle = [(10, 10),
            (40, 20),
            (20, 40)]
triangle2 = [(10, 10),
            (20, 40),
            (5, 45)]

def set_at(pos, color):
    x, y = int(pos[0]), int(pos[1])
    display_buffer[x+y*width] = (int(cval) for cval in color)

def edge_function(a, b, p):
    return (b[1] - a[1]) * (p[0] - a[0]) - (b[0] - a[0]) * (p[1] - a[1])

def get_triangle(vectors):
    a, b, c = vectors
    min_x = int(min(a[0], b[0], c[0]))
    max_x = int(max(a[0], b[0], c[0]))
    min_y = int(min(a[1], b[1], c[1]))
    max_y = int(max(a[1], b[1], c[1]))

    area = edge_function(a, b, c)
    if area < 0:
        inside = lambda e: e <= 0
    else:
        inside = lambda e: e >= 0

    pixels = []
    for x in range(min_x, max_x+1):
        for y in range(min_y, max_y+1):
            P = (x, y)
            if (inside(edge_function(a, b, P)) and
                inside(edge_function(b, c, P)) and
                inside(edge_function(c, a, P))):
                pixels.append(P)
    return pixels

triangle_boundingbox = get_triangle(triangle)
triangle_boundingbox2 = get_triangle(triangle2)
    
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    for x in range(width):
        for y in range(height):
            nx = x / width
            ny = y / height
            set_at((x, y), (255*nx, 255*ny, 255))
            
    display_data = bytes(color for (r, g, b) in display_buffer for color in (r, g, b))
    dwin.blit(pygame.image.frombuffer(display_data, (width, height), "RGB"), (0, 0))
    for pos in triangle_boundingbox: # Triangle's background box
        dwin.set_at(pos, (150, 150, 150))
    for pos in triangle_boundingbox2: # Triangle's background box
        dwin.set_at(pos, (80, 80, 80))
    # pygame.draw.polygon(dwin, (100, 0, 0), triangle)

    transformed_display = pygame.transform.scale(dwin, win.get_size())
    win.blit(transformed_display, (0, 0))
    
    pygame.display.update()
    clock.tick()
    CFPS = clock.get_fps()
    pygame.display.set_caption(f"FPS: {CFPS:.1f}")