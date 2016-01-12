import pygame
import os.path
import math
import json
import time


def bases(n):
    tmp = [[0 for i in range(n)] for i in range(n)]
    return tmp


def render(rotation):
    screen.fill(BLACK)
    if STEP == 2:
        draw_arrow()
    draw_plateau(plateau, rotation)
    if STEP == 1 and not animation:
        screen.blit(img[PLAYER], pygame.rect.Rect(
            mouse_pos[0] - 15, mouse_pos[1] - 15, 30, 30))
    if screen_size[1] <= mouse_pos[0] <= screen_size[1] + 250 - padding_step_1 and padding_step_1 + 146 + padding_step_1 <= mouse_pos[1] <= padding_step_1 + 45 + 146 + padding_step_1:
        draw_button_reset(1)
    else:
        draw_button_reset(0)
    who_play()
    if STEP == 3:
        animat_win()
    pygame.display.flip()


# numeros des cotes
#  ___
# |1|3|
# |2|4|
#  ---
#
# rotation d'un plateau
# rotation_plateau(liste, nombre_de_ligne, numero_du_cote, True = horaire
# et False = antihoraire)
def rotation_plateau(plateau_tmp, m, n, sens):
    x, y, maxx, maxy = 0, 0, m // 2, m // 2

    if n % 2 == 0:
        x = m // 2
        maxx = m
    if n > 2:
        y = m // 2
        maxy = m
    tmp = [[0 for i in range(m // 2)] for i in range(m // 2)]
    tmpy = maxy
    while tmpy > y:
        tmpx = maxx
        while tmpx > x:
            if not sens:
                tmp[maxy - tmpy][tmpx - x - 1] = plateau_tmp[tmpx - 1][tmpy - 1]
            else:
                tmp[tmpy - y - 1][maxx - tmpx] = plateau_tmp[tmpx - 1][tmpy - 1]
            tmpx -= 1
        tmpy -= 1

    for nx, vx in enumerate(tmp):
        for ny, vy in enumerate(vx):
            plateau_tmp[nx + x][ny + y] = vy

    return plateau_tmp


def draw_arrow():
    height = screen_size[1] - (padding_step_2 * 2)
    screen.blit(img_arrow, (padding_step_2, padding_step_2 - 30))
    screen.blit(pygame.transform.flip(img_arrow, True, False),
                (padding_step_2 - 30 + height, padding_step_2 - 30))
    screen.blit(pygame.transform.flip(pygame.transform.rotate(
        img_arrow, 90), True, True), (padding_step_2 + height, padding_step_2))
    screen.blit(pygame.transform.flip(pygame.transform.rotate(img_arrow, 90),
                                      True, False), (padding_step_2 + height, padding_step_2 + height - 30))
    screen.blit(pygame.transform.flip(img_arrow, True, True),
                (padding_step_2 + height - 30, padding_step_2 + height))
    screen.blit(pygame.transform.flip(img_arrow, False, True),
                (padding_step_2, padding_step_2 + height))
    screen.blit(pygame.transform.rotate(img_arrow, 90),
                (padding_step_2 - 30, padding_step_2 + height - 30))
    screen.blit(pygame.transform.flip(pygame.transform.rotate(
        img_arrow, 90), False, True), (padding_step_2 - 30, padding_step_2))


def click_arrows(mouse_pos):
    global plateau
    global columns
    global STEP
    global PLAYER
    height = screen_size[1] - (padding_step_2 * 2)
    x, y = mouse_pos[0], mouse_pos[1]
    action = False
    rotation = False
    cadrant = 1
    if padding_step_2 + 30 >= x >= padding_step_2 >= y >= padding_step_2 - 30:
        cadrant = 1
        rotation = True
        action = True
    elif padding_step_2 + height >= x >= padding_step_2 + height - 30 and padding_step_2 >= y >= padding_step_2 - 30:
        cadrant = 3
        action = True
    elif padding_step_2 + height + 30 >= x >= padding_step_2 + height and padding_step_2 + 30 >= y >= padding_step_2:
        cadrant = 3
        rotation = True
        action = True
    elif padding_step_2 + height + 30 >= x >= padding_step_2 + height >= y >= padding_step_2 + height - 30:
        cadrant = 4
        action = True
    elif padding_step_2 + height + 30 >= y >= padding_step_2 + height >= x >= padding_step_2 + height - 30:
        cadrant = 4
        rotation = True
        action = True
    elif padding_step_2 + 30 >= x >= padding_step_2 and padding_step_2 + height + 30 >= y >= padding_step_2 + height:
        cadrant = 2
        action = True
    elif padding_step_2 >= x >= padding_step_2 - 30 and padding_step_2 + height >= y >= padding_step_2 + height - 30:
        cadrant = 2
        rotation = True
        action = True
    elif padding_step_2 + 30 >= y >= padding_step_2 >= x >= padding_step_2 - 30:
        cadrant = 1
        rotation = False
        action = True

    if action:
        sound[0].play()
        render((0, 0))
        STEP = 1
        if rotation:
            angle = 90
        else:
            angle = -90
        rotate_cadrant(time.time() * 1000, cadrant, angle, 1000)
        plateau = rotation_plateau(plateau, columns, cadrant, rotation)
        resize_plateau(time.time() * 1000,
                       padding_step_1 - padding_step_2, 600)
        save()
        if test_win(columns, plateau, nbr_pion, PLAYER):
            STEP = 3
        else:
            PLAYER = 1 if PLAYER == 2 else 2


# position d'un point après rotation
def point_rotate(cx, cy, x, y, angle):
    radians = (math.pi / 180) * -angle
    cos = math.cos(radians)
    sin = math.sin(radians)
    nx = (cos * (x - cx)) + (sin * (y - cy)) + cx
    ny = (cos * (y - cy)) - (sin * (x - cx)) + cy
    return nx, ny


def draw_plateau(plateau, rotate):
    height = screen_size[1]
    height_cadrant = round((height - padding * 2) / 2)
    mid_GUTTER = round(GUTTER / 2)

    if rotate[0] == 1 and rotate[1] != 0:
        cx, cy = padding + ((height_cadrant - mid_GUTTER) //
                            2), padding + ((height_cadrant - mid_GUTTER) // 2)
        pos_cadrant = (
            point_rotate(cx, cy, padding, padding, rotate[1]),
            point_rotate(cx, cy, padding + height_cadrant -
                         mid_GUTTER, padding, rotate[1]),
            point_rotate(cx, cy, padding + height_cadrant - mid_GUTTER,
                         padding + height_cadrant - mid_GUTTER, rotate[1]),
            point_rotate(cx, cy, padding, padding +
                         height_cadrant - mid_GUTTER, rotate[1])
        )
    else:
        pos_cadrant = (
            (padding, padding),
            (padding + height_cadrant - mid_GUTTER, padding),
            (padding + height_cadrant - mid_GUTTER,
             padding + height_cadrant - mid_GUTTER),
            (padding, padding + height_cadrant - mid_GUTTER)
        )
    pygame.draw.polygon(screen, RED, pos_cadrant)

    if rotate[0] == 3 and rotate[1] != 0:
        cx, cy = padding + height_cadrant + \
            ((height_cadrant + mid_GUTTER) // 2), padding + \
            ((height_cadrant - mid_GUTTER) // 2)
        pos_cadrant = (
            point_rotate(cx, cy, padding + height_cadrant +
                         mid_GUTTER, padding, rotate[1]),
            point_rotate(cx, cy, padding + height_cadrant +
                         height_cadrant, padding, rotate[1]),
            point_rotate(cx, cy, padding + height_cadrant + height_cadrant,
                         padding + height_cadrant - mid_GUTTER, rotate[1]),
            point_rotate(cx, cy, padding + height_cadrant + mid_GUTTER,
                         padding + height_cadrant - mid_GUTTER, rotate[1])
        )
    else:
        pos_cadrant = (
            (padding + height_cadrant + mid_GUTTER, padding),
            (padding + height_cadrant + mid_GUTTER +
             height_cadrant - mid_GUTTER, padding),
            (padding + height_cadrant + mid_GUTTER + height_cadrant -
             mid_GUTTER, padding + height_cadrant - mid_GUTTER),
            (padding + height_cadrant + mid_GUTTER,
             padding + height_cadrant - mid_GUTTER)
        )
    pygame.draw.polygon(screen, RED, pos_cadrant)

    if rotate[0] == 4 and rotate[1] != 0:
        cx, cy = padding + height_cadrant + \
            ((height_cadrant + mid_GUTTER) // 2), padding + \
            height_cadrant + ((height_cadrant + mid_GUTTER) // 2)
        pos_cadrant = (
            point_rotate(cx, cy, padding + height_cadrant + mid_GUTTER,
                         padding + height_cadrant + mid_GUTTER, rotate[1]),
            point_rotate(cx, cy, padding + height_cadrant + mid_GUTTER + height_cadrant -
                         mid_GUTTER, padding + height_cadrant + mid_GUTTER, rotate[1]),
            point_rotate(cx, cy, padding + height_cadrant + mid_GUTTER + height_cadrant - mid_GUTTER,
                         padding + height_cadrant + mid_GUTTER + height_cadrant - mid_GUTTER, rotate[1]),
            point_rotate(cx, cy, padding + height_cadrant + mid_GUTTER, padding +
                         height_cadrant + mid_GUTTER + height_cadrant - mid_GUTTER, rotate[1])
        )
    else:
        pos_cadrant = (
            (padding + height_cadrant + mid_GUTTER,
             padding + height_cadrant + mid_GUTTER),
            (padding + height_cadrant + mid_GUTTER + height_cadrant -
             mid_GUTTER, padding + height_cadrant + mid_GUTTER),
            (padding + height_cadrant + mid_GUTTER + height_cadrant - mid_GUTTER,
             padding + height_cadrant + mid_GUTTER + height_cadrant - mid_GUTTER),
            (padding + height_cadrant + mid_GUTTER, padding +
             height_cadrant + mid_GUTTER + height_cadrant - mid_GUTTER)
        )
    pygame.draw.polygon(screen, RED, pos_cadrant)

    if rotate[0] == 2 and rotate[1] != 0:
        cx, cy = padding + ((height_cadrant - mid_GUTTER) // 2), padding + \
            height_cadrant + ((height_cadrant + mid_GUTTER) // 2)
        pos_cadrant = (
            point_rotate(cx, cy, padding, padding +
                         height_cadrant + mid_GUTTER, rotate[1]),
            point_rotate(cx, cy, padding + height_cadrant - mid_GUTTER,
                         padding + height_cadrant + mid_GUTTER, rotate[1]),
            point_rotate(cx, cy, padding + height_cadrant - mid_GUTTER, padding +
                         height_cadrant + mid_GUTTER + height_cadrant - mid_GUTTER, rotate[1]),
            point_rotate(cx, cy, padding, padding + height_cadrant +
                         mid_GUTTER + height_cadrant - mid_GUTTER, rotate[1])
        )
    else:
        pos_cadrant = (
            (padding, padding + height_cadrant + mid_GUTTER),
            (padding + height_cadrant - mid_GUTTER,
             padding + height_cadrant + mid_GUTTER),
            (padding + height_cadrant - mid_GUTTER, padding +
             height_cadrant + mid_GUTTER + height_cadrant - mid_GUTTER),
            (padding, padding + height_cadrant +
             mid_GUTTER + height_cadrant - mid_GUTTER)
        )
    pygame.draw.polygon(screen, RED, pos_cadrant)

    height_square = ((height - (padding * 2)) / len(plateau))
    for iy, y in enumerate(plateau):
        for ix, x in enumerate(y):

            if ix < (len(y) + 1) // 2:
                addx = -GUTTER // 4
            else:
                addx = GUTTER // 4

            if iy < (len(y) + 1) // 2:
                addy = -GUTTER // 4
            else:
                addy = GUTTER // 4

            draw_x = ((ix * height_square) + padding + addx) + \
                (height_square - 30) / 2
            draw_y = ((iy * height_square) + padding + addy) + \
                (height_square - 30) / 2

            if rotate[1] != 0 and rotate[0] != 0:
                pos_pion = 1
                #  ___
                # |1|3|
                # |2|4|
                #  ---
                if ix >= (len(y) + 1) // 2:
                    pos_pion += 2
                if iy >= (len(y) + 1) // 2:
                    pos_pion += 1
                if pos_pion == rotate[0]:
                    new_pos_pion = point_rotate(
                        cx, cy, draw_x + 15, draw_y + 15, rotate[1])
                    draw_x = new_pos_pion[0] - 15
                    draw_y = new_pos_pion[1] - 15

            screen.blit(img[x], (draw_x, draw_y))


# retourne la position du click tel que :
# pos = pos_click_plateau(mouse_pos)
# y = pos[0]
# x = pos[1]
# et donc :
# plateau[y][x]
# retourne la valeur de la case cliquee
def pos_click_plateau(pos):
    height = screen_size[1]
    height_cadrant = round((height - padding * 2) / 2)
    x, y = pos[0] - padding, pos[1] - padding
    height_square = round(((height - (padding * 2) - GUTTER) / len(plateau)))
    if y >= height_cadrant - GUTTER / 2:
        if height_cadrant + GUTTER / 2 > y:
            y = -1
        else:
            y -= GUTTER // 2

    if x >= height_cadrant - GUTTER / 2:
        if height_cadrant + GUTTER / 2 > x:
            x = -1
        else:
            x -= GUTTER // 2
    x //= height_square
    y //= height_square
    if columns > x >= 0 and columns > y >= 0:
        return round(x), round(y)
    return -1, -1


def resize_plateau(start, end_value, duration):
    global padding
    global animation
    global mouse_pos
    mouse_pos = (-100, -100)
    start_value = padding
    current_time = time.time() * 1000
    animation = True
    while current_time - start <= duration:
        current_time = time.time() * 1000
        padding = round(ease(current_time - start,
                             start_value, end_value, duration))
        render((0, 0))
    animation = False


def rotate_cadrant(start, cadrant, end_value, duration):
    global padding
    global animation
    global mouse_pos
    mouse_pos = (-100, -100)
    start_value = 0
    current_time = time.time() * 1000
    animation = True
    while current_time - start <= duration:
        current_time = time.time() * 1000
        render(
            (cadrant, round(ease(current_time - start, start_value, end_value, duration))))
    animation = False


# t: temps actuel, b: valeur de depart, c: valeur finale, d: duree
def ease(t, b, c, d):
    t = t / d - 1
    return c * (t * t * t + 1) + b


def save():
    file = open("cache", "w")
    data = {'plateau': plateau, 'step': STEP, 'player': PLAYER}
    file.write(json.dumps(data))
    file.close()


def load():
    global PLAYER
    global plateau
    global STEP
    global columns
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
                        columns = len(plateau)
        file.close()


def new_game():
    global PLAYER
    global plateau
    global STEP
    global columns

    file = open("cache", "w")
    file.write("")
    file.close()

    STEP = 1
    PLAYER = 1 if PLAYER == 2 else 2
    plateau = bases(columns)
    render((0, 0))
    if padding != padding_step_1:
        resize_plateau(time.time() * 1000,
                       padding_step_1 - padding_step_2, 300)


def pose_pion(mouse_pos, player):
    pos = pos_click_plateau(mouse_pos)
    x = pos[0]
    y = pos[1]
    if plateau[y][x] == 0 and x != -1:
        global STEP
        sound[0].play()
        plateau[y][x] = player
        STEP = 2
        resize_plateau(time.time() * 1000,
                       padding_step_2 - padding_step_1, 600)
        save()
    if test_win(columns, plateau, nbr_pion, player):
        STEP = 3

# n = (int) nombre de colonnes
# l = (list) plateau
# p = (int) nombre de valeur identique à aligner pour une victoire
# j = (int) 1 pour le joueur 1, 2 pour le joueur 2


def draw_button_reset(x):
    screen.blit(img_button_reset[x], (screen_size[
                1], padding_step_1 + 146 + padding_step_1))


def who_play():
    screen.blit(img_turn[PLAYER - 1], (screen_size[1], padding_step_1))


def victory_horizontal(n, l, p, j):
    for y in range(n):
        v = 0
        for x in range(n):
            if l[y][x] == j:
                v += 1
            else:
                v = 0
            if v >= p:
                return True
    return False


def victory_vertical(n, l, p, j):
    for x in range(n):
        v = 0
        for y in range(n):
            if l[y][x] == j:
                v += 1
            else:
                v = 0
            if v >= p:
                return True
    return False


def victory_diagonal1(n, l, p, j):
    for i in range(n * 2):
        x, y, v = i, 0, 0
        while x >= 0 and y < n:
            if n > y >= 0 and n > x >= 0:
                if l[y][x] == j:
                    v += 1
                else:
                    v = 0
                if v >= p:
                    return True
            x -= 1
            y += 1
    return False


def victory_diagonal2(n, l, p, j):
    for i in range(n * 2):
        x, y, v = i, n - 1, 0
        while x >= 0 and y >= 0:
            if n > y >= 0 and n > x >= 0:
                if l[y][x] == j:
                    v += 1
                else:
                    v = 0
                if v >= p:
                    return True
            x -= 1
            y -= 1
    return False


def test_win(n, l, p, j):
    if victory_horizontal(n, l, p, j) or victory_vertical(n, l, p, j) or victory_diagonal1(n, l, p, j) or victory_diagonal2(n, l, p, j):
        file = open("cache", "w")
        file.write("")
        file.close()
        if padding > padding_step_1:
            resize_plateau(time.time() * 1000,
                           padding_step_1 - padding_step_2, 300)
        return True
    return False


def animat_win():
    screen.blit(img_win, (screen_size[1] // 2 - 90, screen_size[1] // 2 - 90))

running = True
RED = (152, 0, 0)
DARK_RED = (131, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GUTTER = 8
PLAYER = 1
STEP = 1
padding_step_1 = 8
padding_step_2 = 45
columns = 6
nbr_pion = 2
mouse_pos = (0, 0)
animation = False
plateau = bases(columns)
reset_step = [[False, 0], [False, 0], [False, 0]]
load()
if STEP == 2:
    padding = padding_step_2
else:
    padding = padding_step_1

pygame.init()
screen_size = (800, 550)
screen = pygame.display.set_mode(screen_size, pygame.RESIZABLE)
clock = pygame.time.Clock()
img = [pygame.image.load(
    'img/0.png'), pygame.image.load('img/1.png'), pygame.image.load('img/2.png')]
img_arrow = pygame.image.load('img/arrow.png')
img_button_reset = [pygame.image.load(
    'img/button_reset.png'), pygame.image.load('img/button_reset_hover.png')]
img_turn = [pygame.image.load('img/turn1.png'),
            pygame.image.load('img/turn2.png')]
img_win = pygame.image.load('img/win.png')
sound = [pygame.mixer.Sound("drop.wav")]
pygame.display.set_caption('Pentago')
render((0, 0))


while running:
    event = pygame.event.wait()
    if event.type == pygame.MOUSEBUTTONUP:
        if screen_size[1] <= pygame.mouse.get_pos()[0] <= screen_size[1] + 250 - padding_step_1 and padding_step_1 + 146 + padding_step_1 <= pygame.mouse.get_pos()[1] <= padding_step_1 + 146 + 45 + padding_step_1:
            sound[0].play()
            new_game()
        if STEP == 1:
            pose_pion(pygame.mouse.get_pos(), PLAYER)
        elif STEP == 2:
            click_arrows(pygame.mouse.get_pos())
    if event.type == pygame.MOUSEMOTION:
        mouse_pos = event.pos
    if event.type == pygame.VIDEORESIZE:
        screen_size = (round(event.size[1] + 250), round(event.size[1]))
        screen = pygame.display.set_mode(screen_size, pygame.RESIZABLE)
    render((0, 0))
    if event.type == pygame.QUIT:
        running = False
pygame.quit()
