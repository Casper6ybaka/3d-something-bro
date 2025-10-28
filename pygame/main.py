import pygame

win = pygame.display.set_mode((500, 500))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    win.fill((255, 255, 140))
    
    pygame.display.update()