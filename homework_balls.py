import pygame
import random

pygame.init()
size = width, height = 400, 300
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
running = True
v = 100
fps = 100
circle_coord = []
circle_color = []
screen2 = pygame.Surface(screen.get_size())
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONUP:
            circle_coord.append(list(event.pos))
            color = "%06x" % random.randint(0, 0xFFFFFF)
            circle_color.append(pygame.Color("#" + str(color)))

    screen2.fill(pygame.Color('black'))
    for i in range(len(circle_coord)):
        pygame.draw.circle(screen2, circle_color[i], (circle_coord[i][0], int(circle_coord[i][1])), 10)
        if circle_coord[i][1] <= 290:
            circle_coord[i][1] += v / fps
    screen.blit(screen2, (0, 0))
    pygame.display.flip()
    clock.tick(fps)

pygame.quit()
