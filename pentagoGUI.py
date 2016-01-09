import pygame
import math
import time


def bases(n):
    plateau = [[0 for i in range(n)] for i in range(n)]
    return plateau


def render():
    screen.fill(BLACK)
    draw_plateau(plateau)
    pygame.display.update()


def draw_plateau(plateau):
    height = screen_size[1]
    height_cadrant = round((height-padding*2)/2)
    mid_GUTTER = round(GUTTER/2)
    pygame.draw.rect(screen, RED, (padding, padding, height_cadrant-mid_GUTTER, height_cadrant-mid_GUTTER), 0)
    pygame.draw.rect(screen, RED, (padding+height_cadrant+mid_GUTTER, padding, height_cadrant-mid_GUTTER, height_cadrant-mid_GUTTER), 0)
    pygame.draw.rect(screen, RED, (padding+height_cadrant+mid_GUTTER, padding+height_cadrant+mid_GUTTER, height_cadrant-mid_GUTTER, height_cadrant-mid_GUTTER), 0)
    pygame.draw.rect(screen, RED, (padding, padding+height_cadrant+mid_GUTTER, height_cadrant-mid_GUTTER, height_cadrant-mid_GUTTER), 0)
    height_square = ((height-(padding*2))/len(plateau))
    for iy, y in enumerate(plateau):
        for ix, x in enumerate(y):

            if ix < (len(y)+1)//2:
                addx = -GUTTER//4
            else:
                addx = GUTTER//4

            if iy < (len(y)+1)//2:
                addy = -GUTTER//4
            else:
                addy = GUTTER//4
            draw_x = ((ix*height_square)+padding+addx)+(height_square-30)/2
            draw_y = ((iy*height_square)+padding+addy)+(height_square-30)/2

            screen.blit(img[x], (draw_x, draw_y))


# retourne la position du click tel que :
# pos = pos_click_plateau(mouse_pos)
# y = pos[0]
# x = pos[1]
# et donc :
# plateau[y][x]
# retourne la valeur de la case cliquée
def pos_click_plateau(pos):
    height = screen_size[1]
    height_cadrant = round((height-padding*2)/2)
    x, y = pos[0]-padding, pos[1]-padding
    height_square = round(((height-(padding*2)-GUTTER)/len(plateau)))
    if y >= height_cadrant-GUTTER/2:
        if height_cadrant+GUTTER/2 > y:
            y = -1
        else:
            y -= GUTTER//2

    if x >= height_cadrant-GUTTER/2:
        if height_cadrant+GUTTER/2 > x:
            x = -1
        else:
            x -= GUTTER//2
    x //= height_square
    y //= height_square
    if columns > x >= 0 and columns > y >= 0:
        return round(x), round(y)
    return -1, -1


def resize_plateau(start, end_value, duration):
    global padding
    start_value = padding
    current_time = time.time()*1000
    while current_time-start <= duration:
        current_time = time.time()*1000
        padding = round(ease(current_time-start, start_value, end_value, duration))
        render()
        clock.tick(FPS)


# t: temps actuel, b: valeur de départ, c: valeur finale, d: durée
def ease(t, b, c, d):
    t = t/d-1
    return -c * (t*t*t*t - 1) + b


def pose_pion(mouse_pos, player):
    pos = pos_click_plateau(mouse_pos)
    x = pos[0]
    y = pos[1]
    if plateau[y][x] == 0 and x != -1:
        global STEP
        plateau[y][x] = player
        render()
        resize_plateau(time.time()*1000, padding_step_2, 600)
        STEP = 2


running = True
RED = (152, 0, 0)
DARK_RED = (131, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
FPS = 60
GUTTER = 6
PLAYER = 1
STEP = 1
padding_step_2 = 60
if STEP == 2:
    padding = padding_step_2
else:
    padding = 20

columns = 6
plateau = bases(columns)

pygame.init()

screen_size = (800, 500)
screen = pygame.display.set_mode(screen_size)
clock = pygame.time.Clock()
img = [pygame.image.load('img/0.png'), pygame.image.load('img/1.png'), pygame.image.load('img/2.png')]
pygame.display.set_caption('Pentago')
render()

while running:
    event = pygame.event.wait()
    if event.type == pygame.MOUSEBUTTONUP:
        if STEP == 1:
            pose_pion(pygame.mouse.get_pos(), PLAYER)
    if event.type == pygame.QUIT:
        running = False
pygame.quit()
