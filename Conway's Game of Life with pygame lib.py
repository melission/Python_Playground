# colour https://developer.mozilla.org/ru/docs/Web/CSS/CSS_Colors/Color_picker_tool

import pygame
from random import randint
from copy import deepcopy

win_resol = width, height = 2000, 1200
tile = 10
w, h = width // tile, height // tile
FPS = 60

pygame.init()
surface = pygame.display.set_mode(win_resol)
clock = pygame.time.Clock()

# works even with more than one current_field
next_field = [[0 for i in range(w)] for j in range(h)]
current_field = [[1 if not (i*j)%120 else 0 for i in range(w)] for j in range(h)]
current_field = [[1 if not i % 12 else 0 for i in range(w)] for j in range(h)]
# current_field = [[randint(0, 1) for i in range(w)] for j in range(h)]
# current_field = [[0 for i in range(w)] for j in range(h)]
# current_field = [[1 if i == w // 2 or j == h // 2 else 0 for i in range(w)] for j in range(h)]
# print('next field array: ', next_field,
#       '\ncurrent field array: ', current_field)


# OFF or ON status
def check_cell(current_field, x, y):
    count = 0
    for j in range(y-1, y+2):
        for i in range(x-1, x+2):
            if current_field[j][i]:
                count += 1

    if current_field[y][x]:
        count -= 1
        if count == 2 or count == 3:
            return 1
        return 0
    else:
        if count == 3:
            return 1
        return 0


while True:
    # colour in RGB in lieu of RGBA
    # background
    surface.fill(pygame.Color(208, 132, 56))
    # if no ON cells than finish
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    # set up lines parameters
    [pygame.draw.line(surface, pygame.Color(208, 132, 56), (x, 0), (x, h)) for x in range(0, w, h)]
    [pygame.draw.line(surface, pygame.Color(208, 132, 56), (0, y), (w, y)) for y in range(0, h, w)]
    # drawing lines
    for x in range(1, w-1):
        for y in range(1, h-1):
            if current_field[y][x]:
                pygame.draw.rect(surface, pygame.Color(150, 208, 56), (x*tile+2, y*tile+2, tile-2, tile-2))
            next_field[y][x] = check_cell(current_field, x, y)

    current_field = deepcopy(next_field)

    print(clock.get_fps())
    pygame.display.flip()
    clock.tick(FPS)

