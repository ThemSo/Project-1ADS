import pygame
import os.path
import json
import time


def bases(n):
    plateau = [[0 for i in range(n)] for i in range(n)]
    return plateau


def render():
    screen.fill(BLACK)
    if STEP == 2:
        draw_arrow()
    draw_plateau(plateau)
    pygame.display.flip()


# numéros des cotés
#  ___
# |1|3|
# |2|4|
#  ---
#
# rotation d'un plateau
# rotation_plateau(liste, nombre_de_ligne, numero_du_cote, True = horaire et False = antihoraire)
def rotation_plateau(plateau, m, n, sens):
    x, y, maxx, maxy = 0, 0, m//2, m//2

    if n % 2 == 0:
        x = m//2
        maxx = m
    if n > 2:
        y = m//2
        maxy = m
    tmp = [[0 for i in range(m//2)] for i in range(m//2)]
    tmpy = maxy
    while tmpy > y:
        tmpx = maxx
        while tmpx > x:
            if not sens:
                tmp[maxy-tmpy][tmpx-x-1] = plateau[tmpx-1][tmpy-1]
            else:
                tmp[tmpy-y-1][maxx-tmpx] = plateau[tmpx-1][tmpy-1]
            tmpx -= 1
        tmpy -= 1

    for nx, vx in enumerate(tmp):
        for ny, vy in enumerate(vx):
            plateau[nx+x][ny+y] = vy

    return plateau


def draw_arrow():
    height = screen_size[1]-(padding_step_2*2)

    screen.blit(img_arrow, (padding_step_2, padding_step_2-30))
    screen.blit(pygame.transform.flip(img_arrow, True, False), (padding_step_2-30+height, padding_step_2-30))
    screen.blit(pygame.transform.flip(pygame.transform.rotate(img_arrow, 90), True, True), (padding_step_2+height, padding_step_2))
    screen.blit(pygame.transform.flip(pygame.transform.rotate(img_arrow, 90), True, False), (padding_step_2+height, padding_step_2+height-30))
    screen.blit(pygame.transform.flip(img_arrow, True, True), (padding_step_2+height-30, padding_step_2+height))
    screen.blit(pygame.transform.flip(img_arrow, False, True), (padding_step_2, padding_step_2+height))

    screen.blit(pygame.transform.rotate(img_arrow, 90), (padding_step_2-30, padding_step_2+height-30))
    screen.blit(pygame.transform.flip(pygame.transform.rotate(img_arrow, 90), False, True), (padding_step_2-30, padding_step_2))


def click_arrows(mouse_pos):
    global plateau
    global columns
    global STEP
    global PLAYER
    height = screen_size[1]-(padding_step_2*2)
    x, y = mouse_pos[0], mouse_pos[1]
    action = False
    if padding_step_2+30 >= x >= padding_step_2 >= y >= padding_step_2-30:
        plateau = rotation_plateau(plateau, columns, 1, True)
        action = True
    elif padding_step_2+height >= x >= padding_step_2+height-30 and padding_step_2 >= y >= padding_step_2-30:
        plateau = rotation_plateau(plateau, columns, 3, False)
        action = True
    elif padding_step_2+height+30 >= x >= padding_step_2+height and padding_step_2+30 >= y >= padding_step_2:
        plateau = rotation_plateau(plateau, columns, 3, True)
        action = True
    elif padding_step_2+height+30 >= x >= padding_step_2+height >= y >= padding_step_2+height-30:
        plateau = rotation_plateau(plateau, columns, 4, False)
        action = True
    elif padding_step_2+height+30 >= y >= padding_step_2+height >= x >= padding_step_2+height-30:
        plateau = rotation_plateau(plateau, columns, 4, True)
        action = True
    elif padding_step_2+30 >= x >= padding_step_2 and padding_step_2+height+30 >= y >= padding_step_2+height:
        plateau = rotation_plateau(plateau, columns, 2, False)
        action = True
    elif padding_step_2 >= x >= padding_step_2-30 and padding_step_2+height >= y >= padding_step_2+height-30:
        plateau = rotation_plateau(plateau, columns, 2, True)
        action = True
    elif padding_step_2+30 >= y >= padding_step_2 >= x >= padding_step_2-30:
        plateau = rotation_plateau(plateau, columns, 1, False)
        action = True

    if action:
        sound[0].play()
        render()
        STEP = 1
        PLAYER = 1 if PLAYER == 2 else 2
        resize_plateau(time.time()*1000, padding_step_1-padding_step_2, 600)
        save()


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
    render()


# t: temps actuel, b: valeur de départ, c: valeur finale, d: durée
def ease(t, b, c, d):
    t = t/d-1
    return c*(t*t*t + 1) + b


def save():
    file = open("cache", "w")
    data = {'plateau': plateau, 'step': STEP, 'player': PLAYER}
    file.write(json.dumps(data))
    file.close()


def load():
    global PLAYER
    global plateau
    global STEP
    if os.path.isfile("cache"):
        file = open("cache", "r")
        data = file.read()
        if data != '':
            data = json.loads(data)
            if 'player' in data and data['player'] != '':
                if 'step' in data and data['step'] != '':
                    if 'plateau' in data and data['plateau'] != '':
                        STEP = data['step']
                        PLAYER = data['player']
                        plateau = data['plateau']
        file.close()


def pose_pion(mouse_pos, player):
    pos = pos_click_plateau(mouse_pos)
    x = pos[0]
    y = pos[1]
    if plateau[y][x] == 0 and x != -1:
        global STEP
        sound[0].play()
        plateau[y][x] = player
        render()
        STEP = 2
        resize_plateau(time.time()*1000, padding_step_2-padding_step_1, 600)
        save()


running = True
RED = (152, 0, 0)
DARK_RED = (131, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
FPS = 60
GUTTER = 8
PLAYER = 1
STEP = 1
padding_step_1 = 8
padding_step_2 = 45
columns = 6
plateau = bases(columns)
load()
if STEP == 2:
    padding = padding_step_2
else:
    padding = padding_step_1

pygame.init()
screen_size = (800, 500)
screen = pygame.display.set_mode(screen_size)
clock = pygame.time.Clock()
img = [pygame.image.load('img/0.png'), pygame.image.load('img/1.png'), pygame.image.load('img/2.png')]
img_arrow = pygame.image.load('img/arrow.png')
sound = [pygame.mixer.Sound("drop.wav")]
pygame.display.set_caption('Pentago')
render()

while running:
    event = pygame.event.wait()
    if event.type == pygame.MOUSEBUTTONUP:
        if STEP == 1:
            pose_pion(pygame.mouse.get_pos(), PLAYER)
        elif STEP == 2:
            click_arrows(pygame.mouse.get_pos())
    if event.type == pygame.QUIT:
        running = False
pygame.quit()
